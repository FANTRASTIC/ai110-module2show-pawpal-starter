# PawPal+ grading self-assessment

This is an evidence-based estimate, not an official grade. CodePath determines
the actual score. Expected points are conservative while personal reflection
review remains outstanding.

| Category | Rubric requirement | Maximum points | Expected points based on verified work | Evidence | Status |
|---|---|---:|---:|---|---|
| UML design | Four classes; relevant attributes/methods; ownership multiplicities; readable final Mermaid source matching code | 4 | 4 | `diagrams/uml_final.mmd` and identical `diagrams/uml.mmd`; draft/final rendered using Mermaid CLI and visually inspected | Pass |
| Core classes | Task details/completion; Pet identity/task management; Owner identity/multiple pets; Scheduler actual cross-pet operations | 4 | 4 | `pawpal_system.py`: `Task`, `Pet`, `Owner`, `Scheduler`; Owner returns `(pet, task)` pairs | Pass |
| Algorithms | At least two correct, reproducible algorithms across pets; all four phase features implemented | 3 | 3 | `sort_by_time`, `filter_tasks`, `mark_task_complete`, `detect_conflicts`; fixed-date backend and UI tests | Pass |
| CLI demo | One owner, two pets, at least three tasks; meaningful algorithm; readable end-to-end output copied into README | 3 | 3 | `main.py`: two pets/four initial tasks; sorting, combined filters, conflict warning, recurring completion and duplicate prevention; README CLI demonstration | Pass |
| Pytest | Test file exists; at least two meaningful tests pass | 3 | 3 | `tests/test_pawpal.py`: 24 cases; `tests/test_app.py`: two workflows; actual result `26 passed in 2.70s` | Pass |
| Documentation and reflection | Classes/algorithms/run instructions; exact pytest command/coverage summary/genuine output; reflection on AI decisions, tradeoffs and verification | 3 | 2 | README includes genuine CLI/pytest evidence and walkthrough; reflection preserves prompts and adds factual notes, but personal judgments are draft answers awaiting student review | Needs work |
| **Total required** | | **20** | **19** | Technical criteria verified; review reflection to target the remaining point | Needs work |

## Integration and submission checks

- CLI: ran successfully with deterministic sample output.
- Tests: 26 passed, covering backend and real Streamlit script reruns.
- Streamlit: launched on port 8501; health endpoint returned HTTP 200.
- Manual browser walkthrough: **Not verified**; UI tool reported no available browsers.
- UML: draft/final rendered successfully with Mermaid CLI; final matched against source.
- Dependencies: no additional application dependencies introduced.
- Generated files: `.venv` and caches are ignored. A starter-tracked `.pyc` was
  removed from the Git index while preserving the local file.
- Repository: intended origin is `FANTRASTIC/ai110-module2show-pawpal-starter`;
  GitHub API returned `private: false`.
- Git: focused commits were created. Final push verification is reported in the
  delivery message after the documentation commit.
- Reflection: confirm proposed personal judgments, add any real rejected suggestion,
  and perform the browser walkthrough before submission.
- Bonus: the possible 10-point rubric was not supplied; no criteria or score invented.
- CodePath Week 5 submission: **Not performed**. The student must explicitly
  authorize submission or complete it themselves.
