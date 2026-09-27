"""Opaque, expiring login sessions for faculty/student collaboration endpoints."""
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Session
from app.db.database import Base, get_db
from app.models.user import User

class PortalSession(Base):
    __tablename__ = 'portal_sessions'
    id = Column(Integer, primary_key=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expires_at = Column(DateTime, nullable=False)

security = HTTPBearer(auto_error=False)

def issue_session(db, user):
    token = secrets.token_urlsafe(32)
    db.add(PortalSession(token_hash=hashlib.sha256(token.encode()).hexdigest(), user_id=user.id,
                        expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return token

def portal_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    if credentials is None:
        raise HTTPException(401, 'Please log out and sign in again to use faculty resources and replies.')
    record = db.query(PortalSession).filter(PortalSession.token_hash == hashlib.sha256(credentials.credentials.encode()).hexdigest(), PortalSession.expires_at > datetime.utcnow()).first()
    user = db.get(User, record.user_id) if record else None
    if not user:
        raise HTTPException(401, 'Session expired. Please sign in again.')
    return user
