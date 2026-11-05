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
