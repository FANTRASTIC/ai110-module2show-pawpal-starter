# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Asked the agent to review my class relationships, help debug recurring tasks, and troubleshoot Streamlit session-state issues after my initial implementation. I would also ask it to suggest edge cases my tests might have missed.

**What did the agent do?**

The agent would review my code, explain potential problems, and suggest focused changes. Its assistance would include checking recurrence date calculations, preventing duplicate occurrences, and helping keep pets and tasks available across Streamlit reruns.

**What did you have to verify or fix manually?**

I would run the tests and CLI, check that completing daily and weekly tasks created the correct next occurrence, and test the interface for sorting, filtering, conflicts, and persistence. I would also compare the UML and documentation with the final code and make sure I understood every suggested change before accepting it.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

I used a focused, step-by-step approach: implement the core classes myself, then asked AI for help with specific issues such as recurrence and Streamlit session state. I accepted suggestions that kept the code readable and matched the assignment requirements, then verify them through tests and interface checks. I chose this approach because it would let me understand and maintain the final implementation while using AI to resolve problems and identify overlooked edge cases.
