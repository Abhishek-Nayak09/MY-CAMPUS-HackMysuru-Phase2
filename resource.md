# Hack Mysuru 1.0 — Phase 2 Submission Index

> **Project:** MY CAMPUS — Personalized Learning for Every Student  
> **Repository:** https://github.com/Abhishek-Nayak09/MY-CAMPUS-HackMysuru-Phase2

---

## 1. Phase 2 Challenge

**Selected challenge:** MY CAMPUS — Personalized / Adaptive Learning

> Official Problem 01 / Problem 02 number can be added here exactly as listed in the Hack Mysuru Phase 2 dashboard.

### Problem

Traditional digital learning usually gives every learner the same content, difficulty and sequence.

Students, however, may:
- already know the basics,
- struggle with one specific concept,
- understand better through visual or interactive learning,
- or remain confused even after digital explanations.

The core gap is that **learning is not personalized**.

### Proposed Solution

MY CAMPUS is a mastery-based adaptive learning platform that understands:

- what a student already knows,
- which concept is weak,
- which learning mode works best,
- and when human faculty support is required.

The learning journey can move through:

```text
Notes → Video → 3D Interactive → Game → AI Tutor → Faculty
```

The learner can stop early and continue to the next topic as soon as the concept is understood.

---

## 2. Working Codebase

The complete Phase 2 MVP codebase is available in this repository.

### Main folders

```text
backend/     FastAPI backend, database models, APIs and services
frontend/    Student/Faculty UI, learning resources, 3D interactives and games
```

### Technology

- Python
- FastAPI
- SQLAlchemy
- HTML5
- CSS3
- JavaScript
- Three.js
- WebGL

Full project overview:

[README.md](./README.md)

---

## 3. Working MVP Demo

### Local MVP

At submission time, the working MVP can be run locally from this repository.

#### Backend

```bash
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

#### Frontend

Open a second terminal:

```bash
cd frontend
..\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:5500/index.html
```

Complete setup instructions are available in:

[README.md — Local MVP Setup](./README.md#9-local-mvp-setup)

> If a cloud deployment is added before final submission, place the public MVP URL here.

---

## 4. Architecture Overview

```text
                         MY CAMPUS
                             │
             ┌───────────────┴───────────────┐
             │                               │
       STUDENT PORTAL                  FACULTY PORTAL
             │                               │
      Adaptive Learning                 Doubt Support
             │                               │
             └───────────────┬───────────────┘
                             │
                         Frontend
                    HTML / CSS / JS
                 Three.js / WebGL
                             │
                          REST API
                             │
                             ▼
                          FastAPI
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
        Auth           Learning APIs       AI / Faculty
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                         SQLAlchemy
                             │
                           Database
```

The architecture connects:

- Student and Faculty authentication
- Course / Subject / Level / Topic learning structure
- Multimodal learning resources
- Adaptive learning preference tracking
- AI Tutor
- AI-to-Faculty escalation
- Faculty doubt ticket workflow

More detail:

[README.md — Architecture Overview](./README.md#5-architecture-overview)

---

## 5. Data Models

Important backend entities include:

- User
- Course
- AcademicYear
- Subject
- Level
- Topic
- LearningContent
- Note
- NoteSection
- DoubtTicket
- StudentLevelProgress
- LevelTestQuestion
- LevelTestAttempt
- LevelTestAnswer

The model supports the learning hierarchy:

```text
Course
  ↓
Academic Year
  ↓
Subject
  ↓
Level
  ↓
Topic
  ↓
Learning Resources
```

and student-side state such as:

```text
Student
  ↓
Learning Progress
  ↓
Resource Attempts
  ↓
Learning Preference
```

See:

[README.md — Main Data Model](./README.md#6-main-data-model)

---

## 6. Key Trade-off Decisions

### Browser-based 3D learning

**Chosen:** Three.js / WebGL  
**Instead of:** requiring a heavy standalone game installation.

**Reason:** Students can use the interactive learning experience directly in the browser.

**Trade-off:** Browser graphics have lower complexity than a full native game engine.

### AI with human escalation

**Chosen:** AI Tutor → Faculty escalation.

**Reason:** AI handles repeated contextual explanations while unresolved learning gaps are handed to a human educator.

**Trade-off:** Final faculty resolution depends on human availability.

### Adaptive preference, not fixed learning labels

**Chosen:** Track which modality works and recommend it earlier in future topics.

**Reason:** A student may learn different concepts through different modalities.

**Trade-off:** Better personalization requires enough learner interaction data.

### Flexible resource journey

**Chosen:**

```text
Notes → Video → Interactive → Game → AI → Faculty
```

with **I Understood → Next Topic** available before completing every resource.

**Reason:** Students are not forced through content they no longer need.

More detail:

[README.md — Key Design Decisions & Trade-offs](./README.md#8-key-design-decisions--trade-offs)

---

## 7. Quick Reviewer Path

1. Open the Student Portal.
2. Register or login as a Student.
3. Select Physics and open a topic.
4. Try Notes, Video, 3D Interactive and Game resources.
5. Use the AI Tutor for additional support.
6. Escalate an unresolved doubt to Faculty.
7. Open the Faculty Portal.
8. View the student's context-aware doubt ticket.

---

## 8. Final Presentation

Final presentation PDF:

[MY CAMPUS — Hack Mysuru Phase 2 Presentation](./presentation/MY_CAMPUS_Phase2_Presentation.pdf)

The presentation covers:

- One Classroom, Many Learning Needs
- Mastery-Based Adaptive Learning Engine
- Student Journey: Test → Learn → Adapt → Escalate
- Faculty & HOD support workflow
- Why MY CAMPUS stands out

---

## 9. Submission Repository

**Public GitHub Repository**

https://github.com/Abhishek-Nayak09/MY-CAMPUS-HackMysuru-Phase2

---

## MY CAMPUS

> **The system learns the learner.**

The platform adapts not only to what students score, but to what they know, where they struggle, and which learning method actually works for them.
