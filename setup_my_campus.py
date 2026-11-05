"""Install a repository-owned environment and safely prepare all bundled content.

Requires Python 3.10+ and network access for the first dependency installation.
No database, user content, or local configuration is reset.
"""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent
ENVIRONMENT = ROOT / '.venv'
PYTHON = ENVIRONMENT / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
STAMP = ENVIRONMENT / '.my-campus-requirements.sha256'
REQUIREMENTS = ROOT / 'requirements.txt'
VALIDATE = (
    "import sys; sys.path.insert(0, 'backend'); "
    "import fastapi,uvicorn,sqlalchemy,httpx,passlib,bcrypt,email_validator,multipart; "
    "assert bcrypt.__version__ == '4.0.1', 'This project requires bcrypt==4.0.1'; "
    "from app.main import app"
)


def run(command):
    subprocess.run([str(part) for part in command], cwd=ROOT, check=True)


def prepare_environment():
    if sys.version_info < (3, 10):
        raise RuntimeError('Install Python 3.10 or newer, then run setup again.')
    if not PYTHON.exists():
        if ENVIRONMENT.exists():
            raise RuntimeError(f'{ENVIRONMENT} exists but has no Python executable. Repair that environment before retrying; it was not deleted.')
        print(f'Creating project environment: {ENVIRONMENT}', flush=True)
        venv.EnvBuilder(with_pip=True).create(ENVIRONMENT)
    digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    valid = subprocess.run([str(PYTHON), '-c', VALIDATE], cwd=ROOT,
                           capture_output=True).returncode == 0
    recorded = STAMP.read_text().strip() if STAMP.exists() else None
    if not valid or recorded != digest:
        print('Installing the repository requirements (first run or dependency update)...', flush=True)
        run([PYTHON, '-m', 'pip', 'install', '--disable-pip-version-check', '-r', REQUIREMENTS])
    run([PYTHON, '-m', 'pip', 'check'])
    run([PYTHON, '-c', VALIDATE])
    # Mark only a fully validated installation; failures are retried next run.
    STAMP.write_text(digest + '\n', encoding='ascii')
    return PYTHON


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true',
                        help='Prepare dependencies without opening or changing the database.')
    args = parser.parse_args()
    try:
        python = prepare_environment()
        if not args.prepare_only:
            run([python, '-X', 'utf8', ROOT / 'setup_demo.py'])
            print('Setup complete: Physics topics, notes, diagrams, videos and quizzes are initialized.', flush=True)
        else:
            print('Project environment is ready.', flush=True)
        print(f'Python: {python}', flush=True)
        print('Start: start_my_campus.bat (Windows), or follow the manual commands in README.', flush=True)
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f'MY CAMPUS setup failed: {error}', file=sys.stderr)
        print('Fix the reported Python/dependency/network error and rerun setup. Existing data was not reset.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
