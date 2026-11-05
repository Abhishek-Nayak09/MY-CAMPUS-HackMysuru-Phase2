# Automatic initialization verification — 6 November 2026

## Cause and implementation

The active default database is `backend/learning.db`. The separate
`backend/learning_backup.db` is a backup, not the configured application database.
Before this change the live DB contained ten topics, four levels, one note with
eight sections, and zero learning-content rows. Startup created tables only.
Missing seed data was the primary reason notes and videos did not appear.

The ten rich-note seeds deleted sections; the resource/test seeds also updated
existing content, and several seeds assumed primary keys 1–10. Root setup simply
ran those scripts in subprocesses, while many scripts swallowed errors and exited
successfully. These entry points now call the centralized initializer. Rich notes,
diagrams, topic definitions, original video guides and questions are static data
under `backend/content/physics/`.

The initializer performs an additive schema migration, transactional insert-only
content synchronization, cross-process locking, missing-asset installation, and
an online backup before first migration. Backend lifespan invokes it before
serving requests. A failed synchronization rolls back rather than publishing
partial curriculum rows. Faculty-authored rows and existing section text are
preserved; missing section orders are filled only in recognized system notes.

The live DB now contains ten topics, four levels, **40 notes, 512 note sections,
ten shared video resources and 30 unlock questions**. All original database rows
were compared to the new pre-migration backup and retained unchanged, including
accounts, scores, attempts, profiles, journeys and sessions. Browser verification
recorded ordinary visits in an existing signed-in session; only those identified
verification rows and counter increments were removed before the final audit.
The original `learning_backup.db` was not overwritten.

## Checks actually performed

- Ten automated initialization/API tests passed in the requested repository.
  Coverage includes fresh/legacy databases; three starts; process concurrency;
  rollback; automatic backups; shifted IDs; missing notes, sections and resources;
  all 40 topic/level note API combinations; diagram file coverage; configured
  video URL formats; student/faculty login; lifespan calls; and the seven-fail /
  eight-pass boundary with incorrect-answer explanations.
- The existing faculty-hub integration script passed against an in-memory copy:
  role/ownership checks, registration/login sessions, resource uploads/downloads,
  locked topics, student doubts, faculty replies, and invalid files.
- Migration was also tested against an isolated copy of the actual populated DB.
  Every original row survived, and second/third initialization changed no rows.
- A real Uvicorn server started with `--reload` against a temporary DB and served
  all topic notes and 30 diagrams. HTTP smoke checks reached index, student and
  faculty dashboards, notes, video, all ten experiment pages and all ten games.
  The detached-console change-trigger probe detected changes but did not finish
  replacing its worker within 20 seconds. That specific background reload cycle
  is not reported as passing. The user's existing interactive `--reload` backend
  did load the changed routes; its live API returned the new ten-topic/four-level
  path. Repeated lifespan and concurrent initialization are separately tested.
- The launcher passed fresh startup/readiness checks on isolated test ports and a
  copied DB. A second invocation reused the exact same process IDs. The original
  8000/5500 services were also reused successfully. HTTP-first detection fixes a
  Windows CIM listener-inventory omission that initially caused a duplicate bind
  attempt; the temporary failed child exited and no duplicate service remained.
- Modified inline JavaScript and shared scripts passed Node syntax checks.
- Browser verification rendered topic 3 Entry notes with all three SVG images
  loaded, then followed Notes → Video → Interactive → Game with level context.
  The topic 3 YouTube player loaded its lesson metadata and Play control. The
  experiment interface and original cargo game loaded successfully.
- Git whitespace checks passed. Database files, backups, private uploads, logs,
  virtual environments and local test data are excluded from the commit.

## Limits

The ten original YouTube lessons are shared across four levels; there are no
forty distinct level-specific recordings. All links are populated, but playback
and embedding have not been verified for every video. Notes remain available as
the fallback. External OpenAI responses require configuration and were not tested.
Every action in every Three.js game was not exercised; static HTTP coverage and
the representative browser route check are the actual game verification scope.
PostgreSQL initialization uses a transaction advisory lock, but migration and
concurrency tests here cover SQLite.

Use `start_my_campus.bat` for one-click Windows startup. Direct Uvicorn commands
remain supported. See README for commands and troubleshooting.
