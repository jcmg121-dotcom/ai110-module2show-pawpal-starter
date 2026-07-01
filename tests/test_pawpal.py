from pawpal_system import Pet, Task, Owner, Scheduler
from datetime import datetime, timedelta


def test_task_mark_complete_updates_status():
    task = Task("task-1", "Feed pet", "Give dinner", "2026-06-29")

    task.mark_complete()

    assert task.status == "completed"


def test_pet_add_task_increases_task_count():
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    task = Task("task-2", "Walk", "Take a walk", "2026-06-29")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_daily_task_next_due_date_is_exactly_one_day_later():
    """Verify that a daily task's next occurrence is exactly 1 day after the current due date using timedelta."""
    daily_task = Task(
        "task-daily",
        "Morning feed",
        "Feed the dog",
        "2026-06-29",
        recurring_interval_days=1,
    )

    next_occurrence = daily_task.create_next_occurrence()

    assert next_occurrence is not None
    assert next_occurrence.due_date == "2026-06-30"
    assert next_occurrence.status == "pending"


def test_weekly_task_next_due_date_is_exactly_seven_days_later():
    """Verify that a weekly task's next occurrence is exactly 7 days after the current due date using timedelta."""
    weekly_task = Task(
        "task-weekly",
        "Weekly vet check",
        "Check vitals",
        "2026-06-29",
        recurring_interval_days=7,
    )

    next_occurrence = weekly_task.create_next_occurrence()

    assert next_occurrence is not None
    assert next_occurrence.due_date == "2026-07-06"
    assert next_occurrence.status == "pending"


def test_recurring_task_creates_next_occurrence():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    owner.add_pet(pet)

    daily_task = Task(
        "task-daily",
        "Morning feed",
        "Feed the dog",
        "2026-06-29",
        duration_minutes=10,
        priority="high",
        recurring_interval_days=1,
    )

    scheduler = Scheduler("schedule-1", owner, pet, "2026-06-29", "2026-06-30")
    scheduler.add_task(daily_task)
    scheduler.generate()

    # Initial list should have 2 occurrences (one for each day)
    initial_count = len(scheduler.tasks)
    assert initial_count >= 2

    # Mark the first occurrence as complete
    first_task = scheduler.tasks[0]
    first_task.complete()

    # The next occurrence should be created
    assert any(task.status == "pending" and "2026-06-30" in task.due_date for task in scheduler.tasks)
