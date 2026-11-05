"""Non-secret identity for distinguishing local project/database instances."""
import hashlib
from sqlalchemy.engine import make_url
from app.db.database import BACKEND_DIR, DATABASE_URL

INSTANCE_ID = hashlib.sha256(
    (str(BACKEND_DIR.resolve()) + '\0' + make_url(DATABASE_URL).render_as_string(hide_password=True)).encode('utf-8')
).hexdigest()[:24]
