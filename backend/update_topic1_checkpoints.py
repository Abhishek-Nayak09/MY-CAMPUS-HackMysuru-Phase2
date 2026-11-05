"""Compatibility entry point; never deletes existing authored checkpoints."""
from app.db.initialize import initialize_database
if __name__ == "__main__":
    print(initialize_database())
