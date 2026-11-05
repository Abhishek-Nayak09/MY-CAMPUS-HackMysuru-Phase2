# Fresh installation and updates

The database is deliberately not committed. The repo includes the content needed
to recreate it: `backend/content/physics/catalog.json`, level notes, thirty SVG
diagrams, the original configured video links and the unlock question bank.
Never copy a private student database into Git to distribute learning content.

## Windows

Install Python 3.10 or newer with its launcher/PATH option. Then:

```powershell
git clone https://github.com/Abhishek-Nayak09/MY-CAMPUS-HackMysuru-Phase2.git
cd MY-CAMPUS-HackMysuru-Phase2
.\setup_my_campus.bat
.\start_my_campus.bat
```

`start_my_campus.bat` also invokes first-time environment preparation if necessary.
Setup creates a repository `.venv`, installs the committed requirements, checks
dependency compatibility and imports, and initializes the database without manual
seed commands. A failed dependency installation is not marked complete; fix the
reported network/Python error and run setup again.

The startup defaults remain frontend `http://127.0.0.1:5500/index.html` and backend
`http://127.0.0.1:8000`. If another checkout or an old backend owns port 8000, the
launcher refuses to reuse it. Stop that server and start from the intended clone;
the launcher never stops an unrelated server for you.

## Pulling updates

```powershell
git pull --ff-only origin main
.\setup_my_campus.bat
.\start_my_campus.bat
```

Restart an already-running backend to load changed code (an interactive Uvicorn
`--reload` process normally does this itself). Setup and startup fill missing
content, preserve existing authored resources, and retain accounts and progress.
They do not reset an existing DB. Managed `.venv` dependency updates use a hash of
the committed requirements. The setup routine does not install into an unrelated
activated Python environment.

Python-only setup is also available: `python setup_my_campus.py`. On Linux/macOS,
use `.venv/bin/python -m uvicorn app.main:app --app-dir backend --port 8000` and,
in another terminal, `.venv/bin/python -m http.server 5500 --directory frontend`.

## Repeatable verification

```powershell
.\.venv\Scripts\python.exe scripts\verify_fresh_install.py
$env:PYTHONPATH = 'backend'
.\.venv\Scripts\python.exe -m unittest discover -s backend/tests -p test_initialization.py -v
.\.venv\Scripts\python.exe -X utf8 backend/tests/test_faculty_hub.py
```

The fresh-install verifier starts real backend/frontend processes on free test
ports with a new disposable database. It does not invoke a seed script. Backend
startup must create the content, and the health response must identify the exact
test database. It checks ten unique topics grouped 2/3/3/2, native notes, thirty
diagram HTTP responses, ten configured video resources, 27 frontend page URLs,
student/faculty registration and login, and all three 8/10 unlock transitions
with incorrect-answer explanations. Two subsequent starts must use new worker
processes while preserving every database row. All test accounts stay in the
disposable DB; the normal `backend/learning.db` is not used by that verifier.

The fourteen unit/integration tests additionally cover missing resources, empty
DB readiness, initialization rollback/concurrency, repeated starts, migration
backups, authored content, shifted IDs and shuffled quiz options. The existing
faculty test uses an in-memory copy of the initialized project DB.

The GitHub workflow `.github/workflows/fresh-install.yml` installs the committed
requirements on clean Windows/Linux runners and runs these checks. A local pass
does not claim the remote workflow has completed; inspect the Actions result for
that commit.

## What readiness means

`/health` reports actual native topic/note/video/question counts and returns HTTP
503 if the expected content is incomplete, instead of declaring an empty DB ready.
An intentionally inactive authored resource can therefore make readiness fail;
it is not reactivated or overwritten automatically. Restore it through the
faculty workflow or check the relevant database configuration.

An explicit `DATABASE_URL` overrides the default absolute `backend/learning.db`.
Check it if setup and a separately launched backend appear to see different data.
Startup errors are shown in the terminal or `.run/backend.err.log`; dependency
errors are printed during setup. First migration backups stay in the ignored
`backend/backups/` folder. Do not delete the live database to fix missing content.

Video links are shared topic lessons, not forty different level recordings.
YouTube playback depends on external availability; Notes provide the fallback.
External AI requires its API configuration. These checks do not prove every
game interaction, third-party video playback, or external AI responses.
