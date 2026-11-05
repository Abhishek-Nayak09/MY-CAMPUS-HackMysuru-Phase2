"""Exercise real servers with a new disposable DB; never uses the user's DB.

Run from any directory using the project's Python. No manual seed command is run:
Uvicorn lifespan must supply all content, including on repeat starts.
"""
import json
import hashlib
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from contextlib import closing
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def request(base, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(base + path, data=data, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=5) as response:
        body = response.read()
        return json.loads(body) if response.headers.get_content_type() == 'application/json' else body


def snapshot(path):
    with closing(sqlite3.connect(path)) as db:
        names = [row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        return {name: db.execute(f'SELECT * FROM "{name}" ORDER BY 1').fetchall() for name in names}


def start(command, cwd, env, log):
    kwargs = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    return subprocess.Popen(command, cwd=cwd, env=env, stdout=log, stderr=log, **kwargs)


def wait_ready(process, base, path, log_path):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(log_path.read_text(encoding='utf-8', errors='replace'))
        try:
            result = request(base, path)
            if path != '/health' or result.get('content', {}).get('ready'):
                return result
        except (OSError, ValueError):
            pass
        time.sleep(0.1)
    raise RuntimeError('Server readiness timed out: ' + log_path.read_text(encoding='utf-8', errors='replace'))


def stop(process):
    if process is not None and process.poll() is None:
        if os.name == 'nt':
            # The Windows venv redirector may own a child Python process.
            # Stop only this check's process tree, so a restart cannot hit an old worker.
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


def main():
    backend = frontend = None
    with tempfile.TemporaryDirectory(prefix='my-campus-fresh-') as temp:
        directory = Path(temp)
        database = directory / 'first-start.db'
        # This URL is explicitly isolated, regardless of the caller's DATABASE_URL.
        env = dict(os.environ, DATABASE_URL='sqlite:///' + database.as_posix(), PYTHONIOENCODING='utf-8')
        backend_port, frontend_port = free_port(), free_port()
        while backend_port == frontend_port:
            frontend_port = free_port()
        api, web = f'http://127.0.0.1:{backend_port}', f'http://127.0.0.1:{frontend_port}'
        backend_command = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--app-dir', str(ROOT / 'backend'),
                           '--host', '127.0.0.1', '--port', str(backend_port)]
        log_path = directory / 'servers.log'
        with log_path.open('w', encoding='utf-8') as log:
            try:
                assert not database.exists(), 'Fresh verification must start without a database'
                backend = start(backend_command, directory, env, log)
                health = wait_ready(backend, api, '/health', log_path)
                expected_instance = hashlib.sha256((str((ROOT / 'backend').resolve()) + '\0' + env['DATABASE_URL']).encode()).hexdigest()[:24]
                assert health['instance_id'] == expected_instance, 'Verification reached a different database/server'
                assert health['content'] == {'ready': True, 'topics': 10, 'levels': 4, 'notes': 10, 'videos': 10, 'quiz_questions': 30}, health
                assert health.get('instance_id')
                frontend = start([sys.executable, '-m', 'http.server', str(frontend_port), '--bind', '127.0.0.1',
                                  '--directory', str(ROOT / 'frontend')], directory, env, log)
                wait_ready(frontend, web, '/index.html', log_path)
                courses = request(api, '/student/courses')['courses']
                course = next(c for c in courses if c['code'] == 'BE')
                year = next(y for y in request(api, f"/student/courses/{course['id']}/years")['years'] if y['year_number'] == 1)
                subject = next(s for s in request(api, f"/student/courses/{course['id']}/years/{year['id']}/subjects")['subjects'] if s['code'] == 'PHY101')
                path = request(api, f"/student/subjects/{subject['id']}/learning-path")['student_learning_path']
                expected = {'Entry': [1, 2], 'Basics': [3, 4, 5], 'Intermediate': [6, 7, 8], 'Pro': [9, 10]}
                seen, assets = [], set()
                for level in path['levels']:
                    assert [t['curriculum_key'] for t in level['topics']] == expected[level['name']]
                    for topic in level['topics']:
                        seen.append(topic['id'])
                        notes = request(api, f"/notes/topic/{topic['id']}?level_id={level['id']}")
                        assert notes['sections'] and notes['note']['title']
                        assets.update(s['media']['url'] for s in notes['sections'] if s['media']['url'])
                        videos = request(api, f"/content/topic/{topic['id']}")['learning_methods']
                        assert any(v['resource_type'] == 'video' and v['resource_url'] for v in videos)
                assert len(seen) == len(set(seen)) == 10
                assert len(assets) == 30
                for url in assets:
                    assert b'<svg' in request(api, url)[:200], url
                for name in ['index.html', 'student.html', 'faculty.html', 'notes.html', 'video.html', 'level-test.html', 'ai_tutor.html',
                             'interactive.html', 'game_topic_1.html'] + [f'interactive_topic_{i}.html' for i in range(2, 11)]:
                    assert request(web, '/' + name), name
                games = list((ROOT / 'frontend/assets/games/physics').glob('*.html'))
                assert len(games) == 9
                for game in games:
                    assert request(web, '/' + game.relative_to(ROOT / 'frontend').as_posix())
                students = {}
                for role in ['student', 'faculty']:
                    login_id = 'fresh_check_' + role
                    students[role] = request(api, '/auth/register', {'full_name': 'Verification ' + role,
                        'login_id': login_id, 'email': role + '@example.com', 'password': 'verification-only-123',
                        'role': role, 'faculty_role': 'professor' if role == 'faculty' else None})['user']
                    login = request(api, '/auth/login', {'login_id': login_id, 'password': 'verification-only-123'})
                    assert login['user']['access_token']
                student_id = students['student']['id']
                status = request(api, f"/level-tests/status/{student_id}/{subject['id']}")
                assert [level['is_unlocked'] for level in status['levels']] == [True, False, False, False]
                for level in path['levels'][:-1]:
                    quiz = request(api, f"/level-tests/test/{student_id}/{level['id']}")
                    assert len(quiz['questions']) == 10 and quiz['required_score'] == 8
                    with closing(sqlite3.connect(database)) as db:
                        correct = dict(db.execute('SELECT id,correct_answer FROM level_test_questions WHERE source_level_id=?', (level['id'],)))
                    answers = [{'question_id': q['id'], 'selected_answer': correct[q['id']] if i < 8 else
                               next(option for option in q['options'] if option != correct[q['id']])}
                               for i, q in enumerate(quiz['questions'])]
                    result = request(api, f"/level-tests/submit/{level['id']}", {'user_id': student_id, 'answers': answers})
                    assert result['passed'] and result['score'] == 8
                    assert len(result['wrong_answers']) == 2 and all(q['explanation'] for q in result['wrong_answers'])
                before = snapshot(database)
                for _ in range(2):
                    previous_pid = health['process_id']
                    stop(backend)
                    backend = start(backend_command, directory, env, log)
                    health = wait_ready(backend, api, '/health', log_path)
                    assert health['instance_id'] == expected_instance
                    assert health['process_id'] != previous_pid, 'Expected a newly started server process'
                    assert before == snapshot(database), 'Restart changed content or student progress'
                print('PASS: empty DB -> real backend startup -> 10 topics in 2/3/3/2 groups; notes, 30 SVGs, 10 video resources; 27 frontend pages; student/faculty login; all three unlock quizzes; two restarts preserve every row.')
                print('All accounts and progress used by this check were confined to its disposable database.')
            finally:
                stop(backend)
                stop(frontend)


if __name__ == '__main__':
    main()
