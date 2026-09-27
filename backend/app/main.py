from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.database import Base, engine


# ============================================================
# IMPORT MODELS
# ============================================================

from app.models.user import User
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic
from app.models.learning_content import LearningContent
from app.models.doubt_ticket import DoubtTicket
from app.models.note import Note, NoteSection

from app.models.personalization import (
    StudentLearningProfile,
    StudentTopicJourney,
    StudentTopicResourceProgress,
)

from app.models.level_test import (
    StudentLevelProgress,
    LevelTestQuestion,
    LevelTestAttempt,
    LevelTestAnswer,
)


# ============================================================
# API ROUTERS
# ============================================================

from app.api import auth
from app.api import student
from app.api import tickets
from app.api import content
from app.api import notes
from app.api import level_tests
from app.api import faculty_hub
from app.api import ai_tutor
from app.api import personalization
from app.api import hod_analytics
from app.api import adaptive_intelligence


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title="My Campus API",

    description=(
        "Personalized and Adaptive Learning Platform "
        "for Hack Mysuru."
    ),

    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# ============================================================
# UPLOADS
# ============================================================

BACKEND_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

UPLOADS_DIR = (
    BACKEND_DIR
    / "uploads"
)

UPLOADS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


app.mount(

    "/uploads",

    StaticFiles(
        directory=str(
            UPLOADS_DIR
        )
    ),

    name="uploads"
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    auth.router
)

app.include_router(
    student.router
)

app.include_router(
    tickets.router
)

app.include_router(
    content.router
)

app.include_router(
    notes.router
)

app.include_router(
    level_tests.router
)

app.include_router(
    faculty_hub.router
)

app.include_router(
    ai_tutor.router
)

app.include_router(
    personalization.router
)

app.include_router(
    hod_analytics.router
)

app.include_router(
    adaptive_intelligence.router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "application":
            "My Campus",

        "status":
            "running",

        "message":
            "Personalized Learning API is active."
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "database":
            "connected",

        "auth_api":
            "active",

        "student_api":
            "active",

        "content_api":
            "active",

        "notes_api":
            "active",

        "tickets_api":
            "active",

        "level_tests_api":
            "active",

        "faculty_hub_api":
            "active",

        "ai_tutor_api":
            "active",

        "personalization_api":
            "active",

        "hod_analytics_api":
            "active",

        "adaptive_intelligence_api":
            "active",

        "uploads":
            "active"
    }