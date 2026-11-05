"""Compatibility entry point; fills missing resources without overwriting edits."""
from app.db.initialize import initialize_database
if __name__ == "__main__":
    print(initialize_database())
