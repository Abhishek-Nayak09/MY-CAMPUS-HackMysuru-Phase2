"""Integration checks use an in-memory COPY of the project DB and temporary uploads."""
import sqlite3
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db, Base
from app.api import faculty_hub
from app.models.topic import Topic
from app.models.level import Level

root = Path(__file__).resolve().parents[1]
source = sqlite3.connect(f'file:{(root / "learning.db").as_posix()}?mode=ro', uri=True)
memory = sqlite3.connect(':memory:', check_same_thread=False)
source.backup(memory)
source.close()
engine = create_engine('sqlite://', creator=lambda: memory, poolclass=StaticPool)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
def database():
    with Session() as db:
        yield db
app.dependency_overrides[get_db] = database
client = TestClient(app)

def register(name, role):
    response = client.post('/auth/register', json=dict(full_name=name, login_id='test_hub_'+name,
        email=name+'@example.com', password='test-only-password-123', role=role,
        faculty_role='professor' if role=='faculty' else None))
    assert response.status_code == 200, response.text
    return {'Authorization': 'Bearer '+response.json()['user']['access_token']}

with tempfile.TemporaryDirectory(prefix='hub-test-', dir=root) as temp:
    faculty_hub.RESOURCE_DIR = Path(temp)
    faculty = register('faculty_one', 'faculty')
    other = register('faculty_two', 'faculty')
    student = register('student_one', 'student')
    stranger = register('student_two', 'student')
    assert client.post('/auth/login',json={'login_id':'test_hub_faculty_one','password':'wrong'}).status_code == 401
    login = client.post('/auth/login',json={'login_id':'test_hub_faculty_one','password':'test-only-password-123'})
    assert login.status_code == 200 and login.json()['user']['access_token']
    assert client.get('/faculty-hub/catalog').status_code == 401
    assert client.get('/faculty-hub/catalog', headers=student).status_code == 403
    catalog = client.get('/faculty-hub/catalog', headers=faculty)
    assert catalog.status_code == 200 and catalog.json()['topics']
    with Session() as db:
        topic = db.query(Topic).join(Level, Topic.level_id==Level.id).filter(Level.is_default_unlocked==True).first()
        locked = db.query(Topic).join(Level, Topic.level_id==Level.id).filter(Level.is_default_unlocked==False).first()
        topic_id, locked_id = topic.id, locked.id
    data={'topic_id':topic_id,'title':'Test handout','resource_type':'notes','description':'Integration test'}
    upload=client.post('/faculty-hub/resources',headers=faculty,data=data,files={'file':('lesson.txt',b'Newton: F = ma','text/plain')})
    assert upload.status_code==201,upload.text
    rid=upload.json()['id']
    listing=client.get(f'/faculty-hub/resources/topic/{topic_id}',headers=student)
    assert listing.status_code==200 and any(r['id']==rid for r in listing.json()['resources'])
    download=client.get(f'/faculty-hub/resources/{rid}/download',headers=student)
    assert download.status_code==200 and download.content==b'Newton: F = ma'
    assert client.get(f'/faculty-hub/resources/{rid}/download').status_code==401
    assert client.post('/faculty-hub/resources',headers=student,data=data,files={'file':('a.txt',b'no')}).status_code==403
    assert client.post('/faculty-hub/resources',headers=faculty,data=data,files={'file':('a.html',b'<script>')}).status_code==400
    assert client.post('/faculty-hub/resources',headers=faculty,data={**data,'url':'javascript:alert(1)'}).status_code==400
    assert client.post('/faculty-hub/resources',headers=faculty,data={**data,'url':'https://example.com/lesson'}).status_code==201
    assert client.post('/faculty-hub/resources',headers=faculty,data=data,files={'file':('empty.txt',b'')}).status_code==400
    locked_upload=client.post('/faculty-hub/resources',headers=faculty,data={**data,'topic_id':locked_id},files={'file':('locked.txt',b'locked')})
    assert locked_upload.status_code==201
    assert client.get(f'/faculty-hub/resources/topic/{locked_id}',headers=student).status_code==403
    assert client.get('/faculty-hub/resources/'+str(locked_upload.json()['id'])+'/download',headers=student).status_code==403
    assert client.post('/faculty-hub/doubts',headers=student,json={'topic_id':locked_id,'doubt_text':'Please explain'}).status_code==403
    doubt=client.post('/faculty-hub/doubts',headers=student,json={'topic_id':topic_id,'doubt_text':'Why does acceleration fall as mass rises?'})
    assert doubt.status_code==201,doubt.text
    tid=doubt.json()['ticket']['id']
    assert any(t['id']==tid for t in client.get('/faculty-hub/tickets',headers=faculty).json()['tickets'])
    assert not any(t['id']==tid for t in client.get('/faculty-hub/tickets',headers=stranger).json()['tickets'])
    assert client.patch(f'/faculty-hub/tickets/{tid}/start',headers=faculty).status_code==200
    assert client.patch(f'/faculty-hub/tickets/{tid}/start',headers=other).status_code==409
    assert client.patch(f'/faculty-hub/tickets/{tid}/resolve',headers=student,json={'faculty_response':'fake'}).status_code==403
    assert client.patch(f'/faculty-hub/tickets/{tid}/resolve',headers=other,json={'faculty_response':'wrong owner'}).status_code==409
    answer='For the same net force, a = F/m. Doubling mass halves acceleration.'
    assert client.patch(f'/faculty-hub/tickets/{tid}/resolve',headers=faculty,json={'faculty_response':answer}).status_code==200
    replies=client.get('/faculty-hub/tickets',headers=student).json()['tickets']
    result=next(t for t in replies if t['id']==tid)
    assert result['status']=='resolved' and result['faculty_response']==answer
    original_limit=faculty_hub.MAX_BYTES
    faculty_hub.MAX_BYTES=3
    assert client.post('/faculty-hub/resources',headers=faculty,data=data,files={'file':('big.txt',b'1234')}).status_code==413
    faculty_hub.MAX_BYTES=original_limit
    print('PASS: registration/login sessions; upload/list/download; role/ownership checks; locked topics; complete student doubt → faculty reply → student view; invalid/empty/oversized files. No test accounts or resources were saved to the project database.')
app.dependency_overrides.clear()

