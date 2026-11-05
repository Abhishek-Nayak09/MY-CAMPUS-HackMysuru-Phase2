"""Map database identities to bundled curriculum assets without assuming IDs 1–10."""
import json
from app.db.initialize import CATALOG_DIR
from app.models.topic import Topic

TOPIC_KEYS = {item['title']: item['key'] for item in
              json.loads((CATALOG_DIR / 'catalog.json').read_text(encoding='utf-8'))['topics']}

def topic_navigation(db, topic):
    key = TOPIC_KEYS.get(topic.title)
    following = None
    if key and key < 10:
        title = next(title for title, value in TOPIC_KEYS.items() if value == key + 1)
        following = db.query(Topic).filter_by(subject_id=topic.subject_id, title=title).first()
    return {'curriculum_key': key, 'next_topic_id': following.id if following else None}


def content_status(db):
    """Check usable native resources instead of treating an empty DB as ready."""
    from sqlalchemy import or_
    from app.models.course import Course
    from app.models.year import AcademicYear
    from app.models.subject import Subject
    from app.models.level import Level
    from app.models.note import Note, NoteSection
    from app.models.learning_content import LearningContent
    from app.models.level_test import LevelTestQuestion

    subject = (db.query(Subject).join(Course, Subject.course_id == Course.id)
               .join(AcademicYear, Subject.year_id == AcademicYear.id)
               .filter(Course.code == 'BE', AcademicYear.year_number == 1,
                       Subject.code == 'PHY101').first())
    if subject is None:
        return {'ready': False, 'topics': 0, 'levels': 0, 'notes': 0, 'videos': 0, 'quiz_questions': 0}
    topics = db.query(Topic).filter(Topic.subject_id == subject.id, Topic.title.in_(TOPIC_KEYS)).all()
    level_count = db.query(Level).filter_by(subject_id=subject.id).count()
    notes = videos = 0
    for topic in topics:
        note = db.query(Note).filter(Note.topic_id == topic.id, Note.is_active == True,
            or_(Note.level_id == topic.level_id, Note.level_id.is_(None))).order_by(Note.version.desc()).first()
        if note and db.query(NoteSection.id).filter_by(note_id=note.id, is_active=True).first():
            notes += 1
        if db.query(LearningContent.id).filter(
            LearningContent.topic_id == topic.id, LearningContent.resource_type == 'video',
            LearningContent.is_active == True, LearningContent.resource_url.is_not(None),
            LearningContent.resource_url != '').first():
            videos += 1
    questions = db.query(LevelTestQuestion).filter_by(subject_id=subject.id, is_active=True).count()
    return {'ready': len(topics) == 10 and level_count == 4 and notes == 10 and videos == 10 and questions == 30,
            'topics': len(topics), 'levels': level_count, 'notes': notes, 'videos': videos, 'quiz_questions': questions}
