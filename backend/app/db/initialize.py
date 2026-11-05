"""Transactional, insert-only curriculum initialization, shared by CLI and lifespan."""
import importlib
import json
import logging
import os
import pkgutil
import shutil
import sqlite3
import tempfile
from contextlib import contextmanager, closing
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import inspect, text, or_
from sqlalchemy.orm import Session

from app.db.database import Base, BACKEND_DIR, engine

CATALOG_DIR = BACKEND_DIR / 'content' / 'physics'
log = logging.getLogger(__name__)


def register_models():
    import app.models
    for module in pkgutil.iter_modules(app.models.__path__):
        importlib.import_module('app.models.' + module.name)
    importlib.import_module('app.portal_session')


@contextmanager
def file_lock(path):
    """OS-owned lock releases on process exit, including reload/crash."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            # LK_LOCK retries only ten times; use an explicit bounded timeout.
            import time
            deadline = time.monotonic() + 120
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError('Another MY CAMPUS initializer is still running')
                    time.sleep(0.1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def backup_sqlite(path):
    """SQLite's backup API includes committed WAL data, unlike copying the file."""
    folder = path.parent / 'backups'
    folder.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    destination = folder / f'{path.stem}-before-initialize-{stamp}-{os.getpid()}.db'
    with destination.open('xb'):
        pass
    with closing(sqlite3.connect(f'{path.as_uri()}?mode=ro', uri=True)) as source:
        with closing(sqlite3.connect(destination)) as target:
            source.backup(target)
    log.info('Preserved database backup: %s', destination)
    return destination


def install_assets():
    # Only restore missing bundled assets. Faculty-edited files remain untouched.
    for source in (CATALOG_DIR / 'assets').rglob('*.svg'):
        target = BACKEND_DIR / 'uploads/notes/physics' / source.relative_to(CATALOG_DIR / 'assets')
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output, source.open('rb') as incoming:
                temporary = Path(output.name)
                shutil.copyfileobj(incoming, output)
            os.link(temporary, target)
        except FileExistsError:
            pass
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def ensure(db, model, where, values):
    found = db.query(model).filter_by(**where).first()
    if found is None:
        found = model(**where, **values)
        db.add(found)
        db.flush()
    return found


def sync_catalog(db):
    from app.models.course import Course
    from app.models.year import AcademicYear
    from app.models.subject import Subject
    from app.models.level import Level
    from app.models.topic import Topic
    from app.models.note import Note, NoteSection
    from app.models.learning_content import LearningContent
    from app.models.level_test import LevelTestQuestion

    catalog = json.loads((CATALOG_DIR / 'catalog.json').read_text(encoding='utf-8'))
    focus = json.loads((CATALOG_DIR / 'level_focus.json').read_text(encoding='utf-8'))
    course = db.query(Course).filter(or_(Course.code == 'BE', Course.name == 'Bachelor of Engineering')).first()
    if course is None:
        course = ensure(db, Course, {'code': 'BE'}, {'name': 'Bachelor of Engineering'})
    year = ensure(db, AcademicYear, {'course_id': course.id, 'year_number': 1}, {'name': '1st Year'})
    subject = db.query(Subject).filter(Subject.course_id == course.id, Subject.year_id == year.id,
                                     or_(Subject.code == 'PHY101', Subject.name == 'Physics')).first()
    if subject is None:
        subject = ensure(db, Subject, {'course_id': course.id, 'year_id': year.id, 'code': 'PHY101'}, {'name': 'Physics'})
    levels = {}
    for order, name in enumerate(['Entry', 'Basics', 'Intermediate', 'Pro'], 1):
        levels[name] = ensure(db, Level, {'subject_id': subject.id, 'level_order': order},
                             {'name': name, 'is_default_unlocked': order == 1,
                              'unlock_score_required': 0 if order == 1 else 8})
    topics = {}
    for item in catalog['topics']:
        topic = db.query(Topic).filter_by(subject_id=subject.id, title=item['title']).first()
        if topic is None:
            topic = ensure(db, Topic, {'subject_id': subject.id, 'level_id': levels[item['level']].id,
                                       'topic_order': item['order']},
                           {'title': item['title'], 'description': item['description'],
                            'visualization_type': item['visualization'], 'game_type': item['game']})
            if topic.title != item['title']:
                raise ValueError(f"Curriculum slot conflicts with custom topic: {topic.title}. No data changed.")
        topics[item['key']] = topic
        for name, level in levels.items():
            # A legacy note without level_id belongs to its topic's original level.
            scope = Note.level_id == level.id
            if level.id == topic.level_id:
                scope = or_(scope, Note.level_id.is_(None))
            existing = db.query(Note).filter(Note.topic_id == topic.id, scope).first()
            if existing is None:
                note = Note(topic_id=topic.id, level_id=level.id, created_by=None,
                            **dict(item['note'], title=f"{item['note']['title']} — {name}"))
                db.add(note)
                db.flush()
                existing = note
            if existing.created_by is None and existing.title in (item['note']['title'], f"{item['note']['title']} — {name}"):
                sections = [{'order': 0, 'type': 'concept', 'heading': f'{name}: learning focus',
                             'body': focus[str(item['key'])][name]}] + item['sections']
                present_orders = {row[0] for row in db.query(NoteSection.section_order).filter_by(note_id=existing.id)}
                for section in sections:
                    if section['order'] in present_orders:
                        continue
                    interactive = section.get('interactive')
                    db.add(NoteSection(note_id=existing.id, section_order=section['order'],
                        section_type=section['type'], heading=section.get('heading'), body=section.get('body'),
                        media_url=section.get('media_url'), media_type=section.get('media_type'),
                        caption=section.get('caption'), alt_text=section.get('alt_text'),
                        interactive_data=(interactive if isinstance(interactive, str) else json.dumps(interactive))
                            if interactive else None, is_active=True))
        # The repository's topic videos are shared across levels, not 40 claimed videos.
        video = item['video']
        ensure(db, LearningContent, {'topic_id': topic.id, 'resource_type': 'video'},
               {'title': video.get('video_title', item['title']),
                'description': video.get('video_description', 'Shared topic lesson from the original repository.')
                    + ' External playback and embedding depend on YouTube availability.',
                'resource_url': video.get('youtube_url'), 'content_text': video.get('learning_guide'),
                'content_order': 2, 'is_active': True})
    for test in catalog['tests']:
        source, target = levels[test['source_level']], levels[test['target_level']]
        for question in test['questions']:
            ensure(db, LevelTestQuestion,
                   {'subject_id': subject.id, 'source_level_id': source.id,
                    'target_level_id': target.id, 'question_order': question['order']},
                   {'topic_id': topics[question['topic_id']].id, 'question_text': question['question'],
                    'options_json': json.dumps(question['options']), 'correct_answer': question['answer'],
                    'explanation': question['explanation'], 'concept_gap': question['concept_gap'], 'is_active': True})
    db.flush()
    return {'topics': len(topics), 'levels': len(levels), 'topic_level_notes': 40, 'shared_topic_videos': 10}


def initialize_database(bind=None, *, assets=True):
    bind = bind if bind is not None else engine
    register_models()
    sqlite = bind.dialect.name == 'sqlite'
    path = Path(bind.url.database).resolve() if sqlite and bind.url.database not in (None, '', ':memory:') else None
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
    @contextmanager
    def transaction():
        with bind.connect() as connection:
            if sqlite:
                connection.exec_driver_sql('BEGIN IMMEDIATE')
            elif bind.dialect.name == 'postgresql':
                connection.execute(text('SELECT pg_advisory_xact_lock(735014082)'))
            else:
                raise RuntimeError('Automatic initialization supports SQLite and PostgreSQL only')
            try:
                yield connection
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
    @contextmanager
    def optional_lock():
        if path:
            with file_lock(path.with_suffix(path.suffix + '.initialize.lock')):
                yield
        else:
            yield
    with optional_lock():
        # Back up the pre-migration database exactly once; failures leave no marker.
        if path and path.exists() and path.stat().st_size:
            with closing(sqlite3.connect(f'{path.as_uri()}?mode=ro', uri=True)) as check:
                ready = check.execute("SELECT name FROM sqlite_master WHERE name='campus_initialization'").fetchone()
            if not ready:
                backup_sqlite(path)
        with transaction() as connection:
            Base.metadata.create_all(connection)
            columns = {c['name'] for c in inspect(connection).get_columns('notes')}
            if 'level_id' not in columns:
                connection.exec_driver_sql('ALTER TABLE notes ADD COLUMN level_id INTEGER REFERENCES levels(id)')
            with Session(bind=connection) as db:
                result = sync_catalog(db)
                # flush only: the enclosing transaction owns the commit/rollback.
            if assets:
                install_assets()
            connection.exec_driver_sql('CREATE TABLE IF NOT EXISTS campus_initialization (revision INTEGER PRIMARY KEY)')
            connection.execute(text('INSERT INTO campus_initialization (revision) SELECT 1 WHERE NOT EXISTS (SELECT 1 FROM campus_initialization WHERE revision=1)'))
    log.info('MY CAMPUS curriculum ready: %s', result)
    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(initialize_database())
