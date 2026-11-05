# MY CAMPUS — Personalized Learning for Every Student

> **Hack Mysuru 1.0 · Phase 2 Submission**  
> An adaptive learning platform that understands what a student knows, how they learn best, and when human support is needed.

---

## 1. Problem Understanding

### One Classroom, Many Learning Needs

Traditional digital learning platforms usually deliver the same content, difficulty, and learning sequence to every student.

But students learn differently:

- An advanced learner may be forced to repeat concepts they already understand.
- A struggling learner may repeatedly receive the same explanation.
- A visual learner may be given only text-based notes.
- A student who is still confused may have no structured path to human support.

The key gap is that **learning is not personalized**.

MY CAMPUS is designed to understand:

1. What does the student already know?
2. Which exact concept is weak?
3. Which learning method works best for that student?
4. When should AI stop and a faculty member intervene?

---

## 2. Our Solution

### A Mastery-Based Adaptive Learning Engine

MY CAMPUS continuously personalizes:

- Learning level
- Content format
- Topic progression
- AI support
- Faculty escalation

### Core Learning Flow

```text
SELECT
Course → Year → Subject

        ↓

PLACE
Entry Level / Unlock Assessment

        ↓

LEARN
Notes → Video → 3D Interactive → Game → AI Tutor → Faculty

        ↓

VERIFY
Concept Mastery

        ↓

ADAPT
Preferred learning mode is used to improve future topic journeys
```

The system does not force every learner through the same fixed sequence.

If a student understands a topic after Notes, they can continue to the next topic.

If Notes do not work, the learner can continue through:

```text
Notes
  ↓
Video
  ↓
3D Interactive
  ↓
Game
  ↓
AI Tutor
  ↓
Faculty
```

---

## 3. Key Features

### Student Portal

- Separate Student authentication
- Course, subject and topic learning path
- Level-based learning progression
- Notes
- Video lessons
- Interactive physics experiments
- Three.js / WebGL 3D simulations
- Physics learning games
- AI Tutor
- Faculty escalation
- Learning journey progress
- Preferred-learning-mode tracking

### Mastery Engine

Learning progression is divided into:

```text
ENTRY
BASICS
INTERMEDIATE
PRO
```

Entry is available first.

Higher learning levels are controlled through mastery-based progression.

The planned level-unlock assessment uses:

```text
8 / 10 or higher → Unlock next level
```

Incorrect answers can be connected back to the concepts the learner needs to revisit.

### Learning Preference Engine

The platform tracks which resource type helps a learner understand a concept.

Supported learning modes include:

```text
Notes
Video
3D Interactive
Game
AI Tutor
Faculty
```

The learner is never permanently restricted to one mode.

Instead, preferred modalities can be recommended earlier in future topics.

### Context-Aware AI Tutor

The AI Tutor works within the current topic and uses the available learning context to explain concepts using:

- Simpler explanations
- Real-life examples
- Step-by-step reasoning
- Alternative explanations
- Visual learning support

### Faculty Escalation

If AI support is still not enough, the learner can escalate the doubt to faculty.

Instead of sending only:

> "I don't understand."

the system can provide learning context such as:

- Current topic
- Student's doubt
- Learning resources already attempted
- AI interaction context
- Likely weak concept
- Preferred learning modality

This helps faculty try a different teaching approach instead of repeating the same explanation.

---

## 4. Physics MVP

The current MVP demonstrates the adaptive learning experience using Physics.

### Topic Games

| Topic | Learning Game |
|---|---|
| 1 | Physics introductory learning game |
| 2 | Motion — Bike Race |
| 3 | Forces & Newton's Laws — Cargo Rescue |
| 4 | Work, Energy & Power — Energy Mission |
| 5 | Momentum & Collisions — Collision Arena |
| 6 | Waves, Sound & Vibrations — Resonance Lab |
| 7 | Electricity & Circuits — Campus Power Grid Rescue |
| 8 | Magnetism & Electromagnetism — Magnetic Field Lab |
| 9 | Light & Optics — Optics Lab Rescue |
| 10 | Modern Physics — Quantum Research Lab |

Advanced interactive experiences use **Three.js/WebGL** for browser-based 3D learning.

---

## 5. Architecture Overview

```text
                         MY CAMPUS
                             │
             ┌───────────────┴───────────────┐
             │                               │
       STUDENT PORTAL                  FACULTY PORTAL
             │                               │
             │                               │
     Adaptive Learning                  Doubt Support
             │                               │
             └───────────────┬───────────────┘
                             │
                         Frontend
                    HTML / CSS / JS
                 Three.js / WebGL
                             │
                             │ REST API
                             ▼
                         FastAPI
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
      Auth               Learning APIs        AI / Faculty
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                         SQLAlchemy
                             │
                           Database
```

---

## 6. Main Data Model

The backend is organized around entities such as:

```text
User
 ├── Student
 └── Faculty

Course
  │
Academic Year
  │
Subject
  │
Level
  │
Topic
  ├── Learning Content
  ├── Notes
  ├── Note Sections
  ├── Level Test Data
  └── Doubt / Faculty Support

Student
  │
Learning Progress
  │
Resource Attempts
  │
Learning Preference
```

Main backend models include:

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

---

## 7. Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Three.js
- WebGL
- Browser Local Storage for selected client-side learning state

### Backend

- Python
- FastAPI
- SQLAlchemy
- Uvicorn

### AI

- Context-aware AI tutoring
- Topic-grounded learning assistance
- AI-to-Faculty handoff support

### Development

- VS Code
- Git
- GitHub

---

## 8. Key Design Decisions & Trade-offs

### 1. Browser-Based 3D Instead of Heavy Game Deployment

**Chosen:** Three.js/WebGL

**Reason:** Runs directly inside the learning platform and avoids forcing students to install a separate game application.

**Trade-off:** Browser simulations cannot provide the same graphical complexity as a full native game engine.

### 2. AI Does Not Replace Faculty

**Chosen:** AI → Faculty escalation model

**Reason:** AI handles repeated explanations and contextual support, while unresolved learning gaps are handed to a human educator.

**Trade-off:** Faculty response remains dependent on human availability.

### 3. Learners Are Not Locked Into One Learning Style

**Chosen:** Preference-based recommendation rather than permanent learner labels.

**Reason:** A student may prefer different learning methods for different concepts.

**Trade-off:** Personalization improves only after sufficient learner interaction data is collected.

### 4. Modular Resource Journey

**Chosen:**

```text
Notes → Video → Interactive → Game → AI → Faculty
```

with an option to stop early when the learner understands.

**Reason:** Avoids forcing students through unnecessary content.

---

## 9. Local MVP Setup

### Prerequisites

- Python 3.10+
- Modern browser
- Git

Clone:

```bash
git clone https://github.com/Abhishek-Nayak09/MY-CAMPUS-HackMysuru-Phase2.git
cd MY-CAMPUS-HackMysuru-Phase2
```

Create the Python environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### One-click Windows startup (recommended)

Double-click `start_my_campus.bat`, or run from the repository root:

```powershell
.\start_my_campus.ps1
# Optional: skip browser opening
.\start_my_campus.ps1 -NoBrowser
# Check the environment and port ownership without starting services
.\start_my_campus.ps1 -ValidateOnly
```

The launcher finds an activated environment, a repository `.venv`, or the existing
parent `.venv` (including `C:\hackthon my campus\.venv`). It validates imports,
initializes safely, starts hidden local backend/frontend processes, waits for
readiness, and opens the frontend. It reuses responding MY CAMPUS services on
8000/5500 and rejects unrelated port occupants. Logs are in `.run/`.
No operating-system settings are changed. The batch file uses execution-policy
bypass only for that PowerShell process. If policy disallows it, use the direct
Python commands below.

### Automatic content initialization

FastAPI's lifespan calls `app.db.initialize.initialize_database()` before serving
requests, including when Uvicorn is started directly or with `--reload`. No seed
commands are required. `setup_demo.py` and the legacy `seed_*.py` / video seed
entry points call the same safe initializer for compatibility.

The default database is always `backend/learning.db`, resolved from the backend
source location rather than the shell's working directory. An explicit
`DATABASE_URL` overrides it; use an absolute SQLite path. SQLite URLs supplied
through this variable now receive SQLite's connection settings too. PostgreSQL
URLs remain supported, but this change's automated migration checks cover SQLite.

On the first migration of an existing SQLite database, SQLite's online backup API
creates a unique `backend/backups/learning-before-initialize-*.db`. It includes
committed WAL data and never overwrites `learning_backup.db`. Runtime databases,
sidecars, backups, locks, logs and private faculty uploads are ignored by Git.
Stop the backend before manually restoring a backup, and preserve the current DB
and any WAL/SHM files before restoration.

Initialization holds an OS file lock plus a SQLite `BEGIN IMMEDIATE` transaction
(a transaction advisory lock on PostgreSQL). Table creation, the additive nullable
`notes.level_id` migration, and content inserts commit together or roll back.
Readers cannot observe partial content. Reload workers serialize initialization;
process exit releases the lock. Do not delete the lock file while servers run.

The initializer inserts missing rows using course/year/subject/level/topic identity,
not hardcoded primary keys. It never deletes accounts, resets progress, updates
existing note text, or replaces faculty resources. Missing section orders in
recognized system-owned notes are restored; authored and inactive notes/resources
are preserved. Conflicting custom curriculum slots stop startup with an error
instead of silently replacing content. Existing notes without a level retain
their original topic-level meaning. New note requests accept optional `level_id`;
existing API URLs remain valid.

### Content coverage and limits

- The dashboard divides ten Physics topics across four levels without repeats:
  Entry: topics 1–2; Basics: 3–5; Intermediate: 6–8; Pro: 9–10. Each topic uses
  its stored `level_id`, matching the original curriculum and unlock tests.
  Alternate note packages are retained without duplicating dashboard topics.
- Forty note packages combine the original 118 rich sections with distinct level
  explanations, assumptions, formulas and worked examples. Thirty bundled SVGs
  restore missing generated assets without overwriting existing files.
- Ten original YouTube resources are shared across levels. These are ten topic
  videos, not forty level-specific recordings. Their links come from the original
  repository; availability, regional access and embedding are controlled by
  YouTube. Playback has not been verified for every video. The video page offers
  a Notes fallback and explains external availability limits.
- Entry is unlocked by default; higher levels retain the original unlock rules.
  The original three ten-question tests and eight-correct pass threshold remain.
  Their original question scope is unchanged (topics 1–2, 3–5, and 6–8). Incorrect
  answers include explanations. Initialization does not touch attempts or scores.
- Games and experiments keep their existing implementations. Dashboard and shared
  resource routing use curriculum keys for bundled filenames and actual database
  IDs for API calls. Notes and video navigation carry the selected level.
- AI Tutor and faculty support are retained. External OpenAI responses require
  `OPENAI_API_KEY`; the existing local tutor fallback is not an external AI service.

### Verification and troubleshooting

Run the isolated initialization tests from `backend` using the project Python:

```powershell
& 'C:\hackthon my campus\.venv\Scripts\python.exe' -m unittest discover -s tests -p test_initialization.py -v
& 'C:\hackthon my campus\.venv\Scripts\python.exe' -X utf8 tests/test_faculty_hub.py
```

The initialization suite uses temporary databases for fresh starts, three repeat
starts, populated legacy migration and backup, concurrent processes, rollback,
nonstandard IDs, missing content repair, forty note API combinations, bundled
assets, configured video URLs, student/faculty authentication, lifespan startup,
and seven-versus-eight-correct unlock submissions. The faculty test uses an
in-memory copy of the local DB; it does not save test accounts to that database.
These checks do not prove external video playback, external AI availability, or
every interaction in every Three.js game.

If content is missing, restart the backend after updating source, refresh the
dashboard, and confirm that `DATABASE_URL` points to the intended DB. Do not run
old copies of destructive seed scripts. Initialization errors stop startup and
appear in `.run/backend.err.log` or the Uvicorn terminal. For an occupied port,
close the unrelated process yourself; the launcher does not kill it. If an
existing MY CAMPUS server is reused, restart it to load new Python code. For a
missing dependency, install `requirements.txt` into the Python environment printed
by the launcher. Keep `bcrypt==4.0.1` for the existing Passlib integration. For a
blocked video, open Notes; a configured URL does not guarantee playback.

### Start Backend manually

From the project root:

```bash
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

### Start Frontend

Open another terminal from the project root:

```bash
cd frontend
..\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:5500/index.html
```

---

## 10. Quick Reviewer Path

A reviewer can understand the core MY CAMPUS flow quickly by:

1. Open the application.
2. Register or login as a Student.
3. Select the available Physics subject.
4. Open a topic.
5. Explore Notes, Video, 3D Interactive and Game resources.
6. Use the AI Tutor when additional explanation is required.
7. Escalate an unresolved doubt to Faculty.
8. Login through the Faculty portal and view the learning-context ticket.

---

## 11. Repository Structure

```text
HACK_MYSURU_LEARNING/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       └── services/
│
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── games/
│   └── *.html
│
├── PHYSICS_IMPLEMENTATION_REPORT.md
├── requirements.txt
├── resource.md
└── README.md
```

---

## 12. Current MVP Scope

The Phase 2 prototype currently focuses on demonstrating:

- Student / Faculty learning workflow
- Adaptive multimodal resource journey
- Physics learning content
- Browser-based interactive experiments
- 3D educational games
- AI tutoring
- AI-to-Faculty escalation
- Learning preference foundations

Department-level HOD analytics and broader institutional scaling are part of the extended architecture and future roadmap.

---

## 13. Presentation

Final Hack Mysuru presentation:

```text
Presentation artifact will be referenced from resource.md.
```

---

## 14. Submission

**Hack Mysuru 1.0 — Phase 2**

Repository:

```text
https://github.com/Abhishek-Nayak09/MY-CAMPUS-HackMysuru-Phase2
```

---

## MY CAMPUS

> **The system learns the learner.**

Not just what students scored — but what they know, where they struggle, and which learning method actually works for them.
