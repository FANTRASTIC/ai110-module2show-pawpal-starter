# PawPal+ (CodePath AI110 Project 2)

PawPal+ is a Python pet-care scheduler with a Streamlit interface and a reproducible
CLI demonstration. One owner can manage multiple pets, schedule and edit care
activities, complete tasks, and view a combined daily schedule.

## Features

- Add pets with distinct names and record their species.
- Add and edit pending tasks with a description, date, time, duration, priority,
  and once/daily/weekly frequency.
- View tasks in date/time order and filter by pet or completion status.
- Warn about pending tasks with the same scheduled start across all pets.
- Complete a recurring task to create its next incomplete occurrence.
- Keep the owner, pets, and tasks in Streamlit session state across reruns.

Data lasts for the current browser session; there is no file or database storage.
Priority and duration are displayed for the owner's judgment. The scheduler keeps
chosen times; it does not optimize a time budget, reschedule conflicts, or detect
overlapping durations with different start times.

## Architecture

| Class | Responsibility |
|-------|----------------|
| `Owner` | Stores a name and pets; `add_pet()` checks unique names; `get_all_tasks()` combines every pet's tasks. |
| `Pet` | Stores name, species, and tasks; `add_task()` and `list_tasks()` manage the collection. |
| `Task` | Stores description, due date/time, duration, priority, frequency, and completion; validates inputs and implements `mark_complete()`. |
| `Scheduler` | Retrieves tasks through Owner, sorts and filters them, detects conflicts, and handles completion/recurrence. |

Combined schedules use `(pet, task)` tuples, keeping ownership available for filters
and warnings. Mutable collections have independent dataclass default factories.
`Pet.list_tasks()` returns a list copy containing the stored task objects.

The initial design is in [uml_draft.mmd](diagrams/uml_draft.mmd). The final design is
in [uml_final.mmd](diagrams/uml_final.mmd); [uml.mmd](diagrams/uml.mmd) contains the
same final source for compatibility with the starter's filename.
Both draft and final sources were rendered successfully with Mermaid CLI.

## Smarter Scheduling

| Feature | Method | Behavior |
|---------|--------|----------|
| Chronological sorting | `Scheduler.sort_by_time(tasks=None)` | Uses `sorted()` with a date/time key. Equal starts retain insertion order. |
| Filtering | `Scheduler.filter_tasks(pet_name=None, completed=None, tasks=None)` | Retrieves all pets' tasks by default; supports either filter or both together. Pet names match exactly. |
| Daily/weekly recurrence | `Scheduler.mark_task_complete(task)` | Completes the stored task and adds a new task to the same pet, advancing by one or seven days with `timedelta`. |
| Conflict detection | `Scheduler.detect_conflicts(tasks=None)` | Groups pending tasks by identical date/time and returns warnings with pet and task names. |
| Daily/range retrieval | `Scheduler.get_schedule(start_date=None, end_date=None)` | Retrieves all stored tasks, one day, or an inclusive date range, sorted chronologically. |

Recurrence is generated on completion, rather than expanded into an infinite
calendar. Attributes are preserved and the next occurrence starts incomplete.
Repeated completion of the same task creates no duplicates. Use
`Scheduler.mark_task_complete()` for the scheduling workflow:
`Task.mark_complete()` alone only changes the status.
Completed tasks remain available as history and are excluded from conflict warnings.
Date/time values are local, without timezones.

## Installation and setup

Run commands from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate`.
If PowerShell activation is unavailable, use `.\.venv\Scripts\python.exe`
in place of `python`. Dependencies are Streamlit and pytest; the backend uses
only Python's standard library. Mermaid CLI was a temporary verification tool,
not an application dependency.

## Run the application

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, normally http://localhost:8501.

## CLI demonstration

```powershell
python main.py
```

The demo inserts activities out of chronological order for Mochi and Luna.
It uses the fixed date 2026-10-11 so the output is reproducible.
This output was copied from an actual run:

```text
Today's Schedule (fixed demo date: 2026-10-11)
  08:00 | Mochi: Breakfast (10 min, high, daily)
  08:00 | Luna: Medication (5 min, high, once)
  10:00 | Luna: Grooming (15 min, medium, weekly)
  18:00 | Mochi: Evening walk (30 min, high, once)

Pending tasks for Luna:
  Luna: Medication
  Luna: Grooming

Conflict warnings:
  Conflict on 2026-10-11 at 08:00: Mochi: Breakfast; Luna: Medication

Completed Mochi's Breakfast.
Next occurrence: 2026-10-12 at 08:00; completed=False
After repeated completion: 3 tasks for Mochi (no duplicate).
```

## Testing PawPal+

Install dependencies with `python -m pip install -r requirements.txt`, then run:

```powershell
python -m pytest
```

The 24 backend cases in `tests/test_pawpal.py` verify completion, addition,
multi-pet retrieval, sorting dates before times, stable ties, pet/status/combined
filters, daily and weekly recurrence across a year boundary, duplicate prevention,
one-time tasks, exact-start conflicts, completed-task exclusion, empty collections,
date ranges, ownership checks, separate collections, and input validation.

Two Streamlit AppTest workflows in `tests/test_app.py` verify adding multiple pets,
schedule sorting, warnings, filters, recurring completion, persistence across
reruns, editing, and validation without losing existing data.
These are functional interaction tests, rather than screenshot tests.
No percentage coverage was measured.

Actual successful output from the existing virtual environment:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\haran\Documents\CODEPATH\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 26 items

tests\test_app.py ..                                                     [  7%]
tests\test_pawpal.py ........................                            [100%]

============================= 26 passed in 2.70s ==============================
```

Engineering confidence: **4/5 stars**. The core algorithms and real Streamlit
script interactions pass. The server was launched successfully and its health
endpoint returned HTTP 200. Manual browser visual verification remains pending
because the agent's browser tool exposed no available browser. This rating is an
AI-assisted assessment, not the student's personal rating or an official grade.

## Demo Walkthrough

1. Open **Owner details**, enter your name, and click **Save owner**.
2. Under **Pets**, add Mochi as a dog, then Luna as a cat.
3. Add Mochi's Evening walk at 18:00 and daily Breakfast at 08:00 on the same date.
4. Add Luna's Medication at 08:00 on that date. Enter durations and priorities.
5. Set **Schedule date** to that date and click **Generate schedule**. Breakfast
   and Medication appear before Evening walk despite their insertion order.
6. Observe the conflict warning naming both pets' 08:00 tasks. Warnings consider
   all pets on the selected dates, even when the displayed rows are filtered.
7. Choose Luna under **Filter by pet**, then try the **Completion status** filter.
8. Restore **All pets** and **All**. Complete Mochi's Breakfast. Its status changes
   to Completed and tomorrow's incomplete Breakfast is created.
9. Check **Show all stored dates** to see tomorrow's occurrence. A weekly task
   follows the same workflow and advances seven days.
10. Use **Edit a pending task** to change a title, date, time, duration, priority,
    or frequency. Blank titles produce an error and preserve the existing task.

## Reflection and submission

[reflection.md](reflection.md) preserves the original questions and student notes,
adds factual implementation evidence, and labels proposed personal answers for review.

Before submission, review the reflection draft and perform the browser walkthrough.
The intended repository is
[FANTRASTIC/ai110-module2show-pawpal-starter](https://github.com/FANTRASTIC/ai110-module2show-pawpal-starter);
GitHub's repository API confirmed that it is public. Submit through CodePath's
Week 5 interface yourself. No assignment submission has been performed.
Bonus criteria were not supplied, so no bonus score is claimed.
