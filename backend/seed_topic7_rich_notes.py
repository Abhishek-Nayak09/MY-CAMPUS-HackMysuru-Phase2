"""Compatibility entry point; curriculum initialization is automatic at startup."""
from app.db.initialize import initialize_database

if __name__ == "__main__":
    print(initialize_database())
