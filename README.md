# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

These tests cover the core scheduling behaviors of PawPal+, including task sorting, recurring task creation, completion flow, and conflict detection for overlapping preferred times.

Successful test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-7.4.2, py-1.11.0
rootdir: /Users/josemarroquin/Documents/CodePath/AI110/Week 4/Paw_Project/ai110-module2show-pawpal-starter
collected 13 items

tests/test_pawpal.py
tests/test_pawpal_system.py

.............                                                            [100%]
13 passed in 0.01s
```

## 📐 Smarter Scheduling

The scheduler now includes a few lightweight but useful planning behaviors that make the app more practical for everyday pet care.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Task.sort_key()` and `Scheduler.sort_tasks()` | Tasks are ordered by priority, preferred time, and due date so the plan is easier to follow. |
| Filtering behavior | `Scheduler.filter_tasks()` and `Scheduler.filter_tasks_by_status_or_pet()` | Tasks can be filtered by pet and/or completion status to focus on a specific view of the schedule. |
| Conflict detection logic | `Scheduler.detect_conflicts()` and `Scheduler.get_conflict_warning()` | Pending tasks that share the same date and preferred time are flagged, and the scheduler returns a warning message instead of crashing. |
| Recurring task logic | `Task.create_next_occurrence()` and `Scheduler.complete_task()` | When a recurring task is completed, the scheduler creates the next pending occurrence automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
