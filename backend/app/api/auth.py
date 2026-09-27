from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import get_db
from app.models.user import User
from app.portal_session import issue_session


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# REQUEST MODELS
# =========================================================

class RegisterRequest(BaseModel):
    full_name: str
    login_id: str
    email: EmailStr
    password: str
    role: str
    faculty_role: str | None = None


class LoginRequest(BaseModel):
    login_id: str
    password: str


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    role = payload.role.lower().strip()

    if role not in ["student", "faculty"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be student or faculty"
        )


    if role == "faculty":

        if payload.faculty_role not in [
            "professor",
            "hod"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Faculty role must be professor or hod"
            )


    existing_login = (
        db.query(User)
        .filter(User.login_id == payload.login_id)
        .first()
    )

    if existing_login:
        raise HTTPException(
            status_code=400,
            detail="Login ID already exists"
        )


    existing_email = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    hashed_password = pwd_context.hash(
        payload.password
    )


    user = User(
        full_name=payload.full_name,
        login_id=payload.login_id,
        email=payload.email,
        password_hash=hashed_password,
        role=role,
        faculty_role=(
            payload.faculty_role
            if role == "faculty"
            else None
        )
    )


    db.add(user)
    db.commit()
    db.refresh(user)


    return {
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "access_token": issue_session(db, user),
            "full_name": user.full_name,
            "login_id": user.login_id,
            "role": user.role,
            "faculty_role": user.faculty_role
        }
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login_user(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.login_id == payload.login_id)
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Login ID or password"
        )


    if not pwd_context.verify(
        payload.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Login ID or password"
        )


    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "access_token": issue_session(db, user),
            "full_name": user.full_name,
            "login_id": user.login_id,
            "email": user.email,
            "role": user.role,
            "faculty_role": user.faculty_role
        }
    }