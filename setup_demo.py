"""Optional safe setup. Backend startup also performs this automatically."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))
from app.db.initialize import initialize_database
from app.db.database import engine
from app.services.curriculum import content_status
from sqlalchemy.orm import Session

if __name__ == "__main__":
    result = initialize_database()
    with Session(engine) as db:
        readiness = content_status(db)
    if not readiness['ready']:
        raise RuntimeError(f'Learning content is incomplete: {readiness}. Existing authored/inactive content was preserved; check its settings and DATABASE_URL.')
    print(dict(result, content_ready=True))
