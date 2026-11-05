"""Optional safe setup. Backend startup also performs this automatically."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))
from app.db.initialize import initialize_database

if __name__ == "__main__":
    print(initialize_database())
