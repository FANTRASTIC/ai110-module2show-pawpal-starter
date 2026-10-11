# PawPal+ Project Reflection

> AI-assisted draft for student review. The original prompts and initial notes are
> preserved. Technical statements describe work actually performed in this chat.
> Proposed personal judgments are labeled; confirm or revise them before submission.

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    I want Paw Pal+ users to add and manage multiple pets under an owner
    Have different activities succh as feeding, walking medication etc
    View a combined daily schedule to understand what tasks need to be complted for all pets

- What classes did you include, and what responsibilities did you assign to each?
    -Owner: owner's name
    -Pet: stores information about each pet
    -Task: for task, caring description due date
    -Scheduler: for scheduling

Draft expansion: My three core actions are to add and manage pets, schedule care
activities, and view a combined daily schedule. Owner manages a name and pets;
Pet manages identifying information and tasks; Task represents one activity and
its completion status; Scheduler combines tasks from every pet through Owner.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Implementation notes (AI-assisted; student review pending): The three core actions
are adding/managing pets, scheduling care activities, and viewing a combined daily
schedule. The backend uses `(pet, task)` pairs rather than bare tasks so the
schedule retains each pet's identity. Each class owns a separate list using a
dataclass default factory. The student agreed with keeping tasks under pets and
preserving scheduled times during this chat.

Draft response: The implementation refined how task ownership is represented.
Returning `(pet, task)` pairs means sorting does not lose the pet name, and both
filtering and warnings use the same representation. Input validation was added
for blank names/descriptions, invalid durations, priority, and frequency. Pet
names must be distinct so filtering by name is unambiguous.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Draft response: My scheduler considers due dates, due times, completion status,
pet identity, and recurrence frequency. Tasks are ordered by date before time.
Duration and priority are recorded and displayed, but do not move tasks or select
an optimized subset. The supplied phase requirements prioritize predictable
sorting, filtering, recurrence, and exact-start warnings, so those rules drive
the implementation.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Draft response for review: I would keep exact-start conflict detection for this
version because it is easy to explain and test. It catches two activities at
08:00, but misses an 08:00 thirty-minute walk overlapping 08:15 medication.
Interval checks would improve realism, but the assignment says exact matching is
sufficient. Recurrence also advances only after completion, rather than creating
every future occurrence in advance. It keeps the task list small, but means the
application is not a full calendar of future recurring activities.

Algorithm review record: I asked the assistant for alternatives. It suggested
duration-overlap detection and calendar-based recurrence as future improvements,
and recommended the current simpler algorithms for the supplied requirements.
I have not yet supplied a final personal judgment about those alternatives.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Draft response: I gave the AI assistant a detailed prompt covering the rubric,
six phases, required files, verification commands, and rules against fabricated
reflection or test evidence. I supplied the complete instructions after the
attachment ended partway through Phase 4, and asked about alternative algorithms.
The assistant inspected the starter, drafted UML, implemented the backend and UI,
wrote tests, ran the CLI and tests, checked the server, and prepared documentation.
The detailed requirements gave concrete acceptance criteria for that work.

Personal review question: Which part of that prompting process was most useful
to me? There is no evidence of separate AI chat sessions, so none are claimed.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Draft response: I agreed with storing tasks under pets and preserving scheduled
times. The assistant initially proposed expanding recurring activities for a
requested date range and detecting overlapping durations. After I supplied the
full instructions, it revised the implementation to create the next occurrence
on completion and detect exact-start conflicts. This records an actual change
to an AI proposal; it does not claim I personally rejected that earlier design.

Verification performed by the assistant: fixed-date tests check daily and weekly
date arithmetic, preserved attributes, ownership, and duplicate prevention.
Streamlit interaction tests caught an edit-form problem and passed after a fix.
Personal review question: Was there a suggestion I personally rejected or changed?
If so, add the real example and explain my reasoning here.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Draft response: The assistant ran 24 backend cases for completion, task addition,
multiple pets, stable chronological sorting, filters, recurrence, exact conflicts,
empty collections, date ranges, independent lists, and validation. Two Streamlit
AppTest workflows checked adding pets/tasks, editing, schedule display, warnings,
filtering, completion, and state retained across reruns. These tests protect the
connection between objects and UI, rather than only checking printed output.

Actual result: `26 passed in 2.70s` using the existing virtual environment.
The CLI ran successfully with its fixed 2026-10-11 example. Streamlit launched,
and its health endpoint returned HTTP 200. The draft and final Mermaid sources
rendered successfully and were visually inspected by the assistant. No browser
was exposed by the UI tool, so no manual browser walkthrough is claimed.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Proposed judgment for review: I would rate confidence at four out of five because
the automated backend and Streamlit interactions pass, while manual browser
verification remains outstanding. Next I would check the interface in an actual
browser, longer edit/completion sequences, and very large schedules. If interval
conflicts are added, I would test tasks crossing midnight and tasks whose end
exactly matches the next start. This is a proposed rating, not a recorded personal
assessment.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Suggested answer for review: I am most satisfied with the shared backend because
the CLI and Streamlit interface use the same classes and scheduling methods.
The tests show that completing a recurring task retains history and creates one
next occurrence for the correct pet. Confirm that this matches my own judgment.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Suggested answer for review: I would add duration-overlap warnings before adding
more advanced scheduling. It builds on the duration already stored in Task and
addresses a clear limitation. Saving data between sessions would also make the
application more useful. Confirm or replace these priorities.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Suggested answer for review: Clear behavior rules matter as much as class names.
Specifying when recurrence happens and how conflicts are defined makes the design
testable. AI can connect several files, but I still need to understand the code,
review the design, and compare claims against real outputs. Confirm this in my
own words after reviewing the implementation; no personal learning experience is
asserted as established fact by this draft.
