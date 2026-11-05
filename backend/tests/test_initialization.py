"""Run with: python -m unittest discover -s tests -p test_initialization.py -v.

All writes go to temporary databases; no live student accounts are used.
"""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.db.database import Base, get_db
from app.db.initialize import initialize_database, register_models, CATALOG_DIR
from app.main import app
from app.models.note import Note, NoteSection
from app.models.topic import Topic
from app.models.course import Course
from app.models.level import Level
from app.models.subject import Subject
from app.models.learning_content import LearningContent
from app.models.level_test import StudentLevelProgress, LevelTestQuestion


class InitializationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='campus-init-')
        self.path = Path(self.temp.name) / 'learning.db'
        self.engine = create_engine('sqlite:///' + self.path.as_posix(), connect_args={'timeout': 120})
        initialize_database(self.engine, assets=False)
        def database():
            with Session(self.engine) as db:
                yield db
        self.override = dict(app.dependency_overrides)
        app.dependency_overrides[get_db] = database
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.override)
        self.engine.dispose()
        self.temp.cleanup()

    def snapshot(self):
        with self.engine.connect() as connection:
            return {table: connection.execute(text(f'SELECT * FROM "{table}" ORDER BY 1')).fetchall()
                    for table in Base.metadata.tables}

    def register(self, role):
        response = self.client.post('/auth/register', json={
            'full_name': role, 'login_id': role, 'email': role+'@example.com',
            'password': 'test-only-password', 'role': role,
            'faculty_role': 'professor' if role == 'faculty' else None})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()['user']

    def test_fresh_database_and_three_starts(self):
        with Session(self.engine) as db:
            self.assertEqual(db.query(Course).count(), 1)
            self.assertEqual(db.query(Topic).count(), 10)
            self.assertEqual(db.query(Level).count(), 4)
            self.assertEqual(db.query(Note).count(), 40)
            self.assertEqual(db.query(LearningContent).count(), 10)
            self.assertEqual(db.query(LevelTestQuestion).count(), 30)
        before = self.snapshot()
        initialize_database(self.engine, assets=False)
        initialize_database(self.engine, assets=False)
        self.assertEqual(before, self.snapshot())

    def test_all_topic_level_api_content_and_assets(self):
        courses = self.client.get('/student/courses').json()['courses']
        self.assertEqual(len(courses), 1)
        years = self.client.get(f"/student/courses/{courses[0]['id']}/years").json()['years']
        subjects = self.client.get(f"/student/courses/{courses[0]['id']}/years/{years[0]['id']}/subjects").json()['subjects']
        path = self.client.get(f"/student/subjects/{subjects[0]['id']}/learning-path").json()['student_learning_path']
        self.assertEqual([l['is_unlocked'] for l in path['levels']], [True, False, False, False])
        expected_groups = {
            'Entry': [1, 2], 'Basics': [3, 4, 5],
            'Intermediate': [6, 7, 8], 'Pro': [9, 10],
        }
        all_topics = [topic for level in path['levels'] for topic in level['topics']]
        self.assertEqual(len(all_topics), 10)
        self.assertEqual(len({topic['id'] for topic in all_topics}), 10)
        for level in path['levels']:
            self.assertEqual([t['curriculum_key'] for t in level['topics']], expected_groups[level['name']])
            self.assertTrue(all(t['level_id'] == level['id'] for t in level['topics']))
            # Retained alternate notes remain available through the optional API
            # level parameter, but topics appear only once in the learning path.
            for topic in all_topics:
                response = self.client.get(f"/notes/topic/{topic['id']}?level_id={level['id']}")
                self.assertEqual(response.status_code, 200, response.text)
                sections = response.json()['sections']
                self.assertGreater(len(sections), 5)
                self.assertIn(level['name'], sections[0]['heading'])
                for section in sections:
                    url = section['media']['url']
                    if url:
                        self.assertTrue((CATALOG_DIR/'assets'/url.split('/physics/')[1]).is_file(), url)
                videos = self.client.get(f"/content/topic/{topic['id']}").json()['learning_methods']
                video = next(v for v in videos if v['resource_type'] == 'video')
                self.assertRegex(video['resource_url'], r'^https://www.youtube.com/watch\?v=[A-Za-z0-9_-]{11}$')
        self.assertEqual(self.client.get('/notes/topic/99999').status_code, 404)
        self.assertEqual(self.client.get('/notes/topic/1?level_id=99999').status_code, 400)

    def test_auth_progress_and_authored_content_preserved(self):
        user = self.register('student')
        self.register('faculty')
        for role in ['student', 'faculty']:
            login = self.client.post('/auth/login', json={'login_id':role,'password':'test-only-password'})
            self.assertEqual(login.status_code, 200, login.text)
            self.assertTrue(login.json()['user']['access_token'])
            self.assertEqual(self.client.post('/auth/login',json={'login_id':role,'password':'wrong'}).status_code,401)
        with Session(self.engine) as db:
            level=db.query(Level).filter_by(name='Basics').one()
            db.add(StudentLevelProgress(user_id=user['id'], subject_id=level.subject_id,
                                       level_id=level.id, is_unlocked=True, best_score=9))
            note=db.query(Note).first()
            note.created_by=user['id']
            note.title='Faculty-authored replacement title'
            section=db.query(NoteSection).filter_by(note_id=note.id).first()
            section.body='Author-edited explanation'
            video=db.query(LearningContent).first()
            video.resource_url='https://example.com/faculty-lesson'
            db.commit()
        before=self.snapshot()
        for _ in range(3): initialize_database(self.engine, assets=False)
        self.assertEqual(before,self.snapshot())

    def test_missing_content_repaired_without_other_changes(self):
        with Session(self.engine) as db:
            note=db.query(Note).filter(Note.level_id == 4).first()
            db.query(NoteSection).filter_by(note_id=note.id).delete()
            db.delete(note)
            db.query(LearningContent).filter_by(topic_id=10).delete()
            retained=db.query(NoteSection).filter(NoteSection.note_id != note.id).first()
            retained_id=retained.id
            retained.body='Keep this edited section'
            missing=db.query(NoteSection).filter(NoteSection.note_id != note.id,NoteSection.id != retained_id).first()
            missing_note_id,missing_order=missing.note_id,missing.section_order
            db.delete(missing)
            db.commit()
        initialize_database(self.engine, assets=False)
        with Session(self.engine) as db:
            self.assertEqual(db.query(Note).count(),40)
            self.assertEqual(db.query(LearningContent).count(),10)
            self.assertEqual(db.get(NoteSection,retained_id).body,'Keep this edited section')
            self.assertIsNotNone(db.query(NoteSection).filter_by(note_id=missing_note_id,section_order=missing_order).first())

    def test_transaction_rolls_back_on_failure(self):
        before=self.snapshot()
        def fail(db):
            db.add(Course(name='Must roll back',code='ROLLBACK'))
            db.flush()
            raise RuntimeError('injected failure')
        with patch('app.db.initialize.sync_catalog',side_effect=fail):
            with self.assertRaises(RuntimeError): initialize_database(self.engine,assets=False)
        self.assertEqual(before,self.snapshot())

    def test_concurrent_process_initialization(self):
        path=Path(self.temp.name)/'concurrent.db'
        env=dict(os.environ,DATABASE_URL='sqlite:///'+path.as_posix(),PYTHONPATH=str(Path(__file__).resolve().parents[1]))
        command=[sys.executable,'-c','from app.db.initialize import initialize_database; initialize_database(assets=False)']
        def run(_):
            return subprocess.run(command,env=env,capture_output=True,text=True,timeout=90)
        with ThreadPoolExecutor(max_workers=3) as workers:
            for result in workers.map(run,range(3)):
                self.assertEqual(result.returncode,0,result.stderr)
        with closing(sqlite3.connect(path)) as connection:
            self.assertEqual(connection.execute('select count(*) from topics').fetchone()[0],10)
            self.assertEqual(connection.execute('select count(*) from notes').fetchone()[0],40)

    def test_legacy_schema_backup_and_note_preservation(self):
        # Reproduce the pre-change notes schema without exposing any live users.
        path=Path(self.temp.name)/'legacy.db'
        with closing(sqlite3.connect(self.path)) as source, closing(sqlite3.connect(path)) as target:
            source.backup(target)
        with closing(sqlite3.connect(path)) as connection:
            connection.execute('DROP TABLE campus_initialization')
            columns=[c for c in connection.execute('pragma table_info(notes)') if c[1]!='level_id']
            definitions=', '.join(f'"{c[1]}" {c[2]}' + (' PRIMARY KEY' if c[5] else '') for c in columns)
            names=', '.join(f'"{c[1]}"' for c in columns)
            connection.execute(f'CREATE TABLE legacy_notes ({definitions})')
            connection.execute(f'INSERT INTO legacy_notes SELECT {names} FROM notes')
            connection.execute('DROP TABLE notes')
            connection.execute('ALTER TABLE legacy_notes RENAME TO notes')
            # Preserve only the native note to simulate the reported partial DB.
            connection.execute('DELETE FROM note_sections WHERE note_id != 1')
            connection.execute('DELETE FROM notes WHERE id != 1')
            connection.execute("UPDATE notes SET title='Existing custom note' WHERE id=1")
            connection.commit()
        bind=create_engine('sqlite:///'+path.as_posix())
        try:
            initialize_database(bind,assets=False)
            initialize_database(bind,assets=False)
            backups=list((path.parent/'backups').glob('legacy-before-*.db'))
            self.assertEqual(len(backups),1)
            with closing(sqlite3.connect(backups[0])) as backup:
                self.assertNotIn('level_id',[c[1] for c in backup.execute('pragma table_info(notes)')])
            with Session(bind) as db:
                self.assertEqual(db.get(Note,1).title,'Existing custom note')
                self.assertEqual(db.query(Note).count(),40)
        finally: bind.dispose()

    def test_noncanonical_database_ids(self):
        path=Path(self.temp.name)/'shifted.db'
        bind=create_engine('sqlite:///'+path.as_posix())
        register_models()
        Base.metadata.create_all(bind)
        with Session(bind) as db:
            other=Course(id=200,name='Other',code='OTHER')
            db.add(other)
            db.commit()
        try:
            initialize_database(bind,assets=False)
            with Session(bind) as db:
                self.assertGreater(db.query(Course).filter_by(code='BE').one().id,200)
                # Shift actual topic IDs while retaining relational integrity.
                db.execute(text('UPDATE topics SET id=id+100'))
                db.execute(text('UPDATE notes SET topic_id=topic_id+100'))
                db.execute(text('UPDATE learning_contents SET topic_id=topic_id+100'))
                db.execute(text('UPDATE level_test_questions SET topic_id=topic_id+100'))
                db.commit()
            initialize_database(bind,assets=False)
            with Session(bind) as db:
                self.assertEqual(db.query(Topic).count(),10)
                self.assertEqual(db.query(Note).count(),40)
                self.assertTrue(all(q.topic_id>100 for q in db.query(LevelTestQuestion)))
        finally: bind.dispose()

    def test_lifespan_initializes_on_every_start(self):
        with patch('app.main.initialize_database',side_effect=lambda: initialize_database(self.engine,assets=False)) as initialize:
            for _ in range(3):
                with TestClient(app) as client:
                    self.assertEqual(client.get('/health').status_code,200)
            self.assertEqual(initialize.call_count,3)

    def test_health_detects_missing_learning_resources(self):
        healthy = self.client.get('/health').json()
        self.assertEqual(healthy['status'], 'healthy')
        self.assertTrue(healthy['content']['ready'])
        self.assertEqual(healthy['content']['topics'], 10)
        self.assertTrue(healthy['instance_id'])
        with Session(self.engine) as db:
            db.query(LearningContent).filter_by(resource_type='video').update({'is_active': False})
            db.commit()
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 503)
        degraded = response.json()
        self.assertEqual(degraded['status'], 'degraded')
        self.assertFalse(degraded['content']['ready'])
        self.assertEqual(degraded['content']['videos'], 0)
        self.assertEqual(degraded['instance_id'], healthy['instance_id'])

    def test_empty_database_is_not_reported_content_ready(self):
        from app.services.curriculum import content_status
        bind = create_engine('sqlite:///' + (Path(self.temp.name) / 'empty.db').as_posix())
        try:
            Base.metadata.create_all(bind)
            with Session(bind) as db:
                status = content_status(db)
            self.assertFalse(status['ready'])
            self.assertEqual(status['topics'], 0)
            self.assertEqual(status['notes'], 0)
        finally:
            bind.dispose()

    def test_quiz_options_are_shuffled_on_each_request_without_db_changes(self):
        user = self.register('student')
        with Session(self.engine) as db:
            levels = db.query(Level).order_by(Level.level_order).all()
            for level in levels:
                db.add(StudentLevelProgress(user_id=user['id'], subject_id=level.subject_id,
                    level_id=level.id, is_unlocked=True, best_score=0))
            db.commit()
            source_ids = [level.id for level in levels[:-1]]
            bank = {q.id: (json.loads(q.options_json), q.correct_answer)
                    for q in db.query(LevelTestQuestion)}
        before = self.snapshot()
        calls = 0
        def rotate(options):
            # Deterministic permutations keep this regression test non-flaky.
            nonlocal calls
            calls += 1
            shift = calls % len(options)
            options[:] = options[shift:] + options[:shift]
        positions = set()
        with patch('app.api.level_tests.SystemRandom.shuffle', side_effect=rotate) as shuffle:
            for source_id in source_ids:
                batches = []
                for _ in range(2):
                    response = self.client.get(f"/level-tests/test/{user['id']}/{source_id}")
                    self.assertEqual(response.status_code, 200, response.text)
                    questions = response.json()['questions']
                    self.assertEqual(len(questions), 10)
                    batches.append(questions)
                    for question in questions:
                        original, correct = bank[question['id']]
                        self.assertCountEqual(question['options'], original)
                        self.assertNotIn('correct_answer', question)
                        self.assertNotIn('explanation', question)
                        positions.add(question['options'].index(correct))
                self.assertEqual([q['id'] for q in batches[0]], [q['id'] for q in batches[1]])
                self.assertTrue(all(a['options'] != b['options'] for a,b in zip(*batches)))
            self.assertEqual(shuffle.call_count, 60)
        self.assertEqual(positions, {0, 1, 2, 3})
        self.assertEqual(before, self.snapshot())

    def test_shuffled_quiz_submission_still_scores_by_answer_text(self):
        user = self.register('student')
        with Session(self.engine) as db:
            source_id = db.query(Level).filter_by(name='Entry').one().id
            correct = {q.id:q.correct_answer for q in db.query(LevelTestQuestion)
                       .filter_by(source_level_id=source_id)}
        with patch('app.api.level_tests.SystemRandom.shuffle', side_effect=lambda options: options.reverse()):
            response = self.client.get(f"/level-tests/test/{user['id']}/{source_id}")
        self.assertEqual(response.status_code, 200, response.text)
        displayed = response.json()['questions']
        answers = []
        for i, question in enumerate(displayed):
            answer = correct[question['id']]
            self.assertEqual(question['options'][-1], answer)
            selected = answer if i < 8 else next(option for option in question['options'] if option != answer)
            answers.append({'question_id':question['id'], 'selected_answer':selected})
        result = self.client.post(f'/level-tests/submit/{source_id}',
                                 json={'user_id':user['id'], 'answers':answers})
        self.assertEqual(result.status_code, 200, result.text)
        self.assertEqual(result.json()['score'], 8)
        self.assertTrue(result.json()['passed'])
        self.assertEqual(len(result.json()['wrong_answers']), 2)
        self.assertTrue(all(item['explanation'] for item in result.json()['wrong_answers']))

    def test_unlock_rule_and_wrong_answer_explanations(self):
        user=self.register('student')
        with Session(self.engine) as db:
            entry=db.query(Level).filter_by(name='Entry').one()
            entry_id,subject_id=entry.id,entry.subject_id
            questions=db.query(LevelTestQuestion).filter_by(source_level_id=entry_id).order_by(LevelTestQuestion.question_order).all()
            answers=[{'question_id':q.id,'selected_answer':q.correct_answer if i<7 else 'incorrect'} for i,q in enumerate(questions)]
        status=self.client.get(f"/level-tests/status/{user['id']}/{subject_id}")
        self.assertEqual(status.status_code,200,status.text)
        response=self.client.post(f'/level-tests/submit/{entry_id}',json={'user_id':user['id'],'answers':answers})
        self.assertEqual(response.status_code,200,response.text)
        self.assertFalse(response.json()['passed'])
        self.assertTrue(all(a['explanation'] for a in response.json()['wrong_answers']))
        with Session(self.engine) as db:
            eighth=db.get(LevelTestQuestion,answers[7]['question_id'])
            answers[7]['selected_answer']=eighth.correct_answer
        response=self.client.post(f'/level-tests/submit/{entry_id}',json={'user_id':user['id'],'answers':answers})
        self.assertEqual(response.status_code,200,response.text)
        self.assertTrue(response.json()['passed'])
        before=self.snapshot()
        initialize_database(self.engine,assets=False)
        self.assertEqual(before,self.snapshot())


if __name__=='__main__': unittest.main()
