from pawpal_system import Owner, Pet, Scheduler, Task


def test_owner_add_pet_sets_bidirectional_relationship():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)

    owner.add_pet(pet)

    assert pet.owner is owner
    assert pet in owner.pets


def test_scheduler_generate_orders_tasks_by_priority_and_due_date():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    owner.add_pet(pet)

    scheduler = Scheduler("schedule-1", owner, pet, "2026-06-29", "2026-06-29")
    scheduler.add_task(Task("task-1", "Feeding", "Feed breakfast", "2026-06-29", duration_minutes=10, priority="low"))
    scheduler.add_task(Task("task-2", "Morning walk", "Walk the dog", "2026-06-29", duration_minutes=20, priority="high"))
    scheduler.add_task(Task("task-3", "Medication", "Give medicine", "2026-06-29", duration_minutes=5, priority="high"))

    scheduler.generate()

    assert [task.title for task in scheduler.tasks] == ["Morning walk", "Medication", "Feeding"]


def test_scheduler_filters_by_pet_and_status_and_detects_conflicts():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet1 = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    pet2 = Pet("pet-2", "Luna", "cat", "siamese", 2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler("schedule-2", owner, pet1, "2026-06-29", "2026-06-29")
    task1 = Task("task-1", "Morning walk", "Walk Mochi", "2026-06-29", duration_minutes=20, priority="high", preferred_time="08:00")
    task2 = Task("task-2", "Feeding", "Feed Luna", "2026-06-29", duration_minutes=10, priority="medium", preferred_time="08:00")
    task3 = Task("task-3", "Medication", "Give medicine", "2026-06-29", duration_minutes=5, priority="high", preferred_time="09:00")
    task1.pet = pet1
    task2.pet = pet2
    task3.pet = pet1
    task3.mark_complete()

    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    filtered = scheduler.filter_tasks(pet=pet1, status="pending")

    assert [task.title for task in filtered] == ["Morning walk"]
    assert len(scheduler.detect_conflicts()) == 1


def test_scheduler_expands_recurring_tasks_across_date_range():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    owner.add_pet(pet)

    scheduler = Scheduler("schedule-3", owner, pet, "2026-06-29", "2026-07-05")
    recurring_task = Task("task-1", "Feeding", "Feed breakfast", "2026-06-29", duration_minutes=10, priority="medium", preferred_time="07:00", recurring_interval_days=2)
    scheduler.add_task(recurring_task)

    scheduler.generate()

    assert len(scheduler.tasks) == 4
    assert [task.due_date for task in scheduler.tasks[:3]] == ["2026-06-29", "2026-07-01", "2026-07-03"]


def test_completed_recurring_task_creates_next_occurrence():
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")
    pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    owner.add_pet(pet)

    scheduler = Scheduler("schedule-4", owner, pet, "2026-06-29", "2026-07-05")
    task = Task("task-1", "Feeding", "Feed breakfast", "2026-06-29", duration_minutes=10, priority="medium", preferred_time="07:00", recurring_interval_days=1)
    scheduler.add_task(task)
    scheduler.generate()

    task_to_complete = next(task for task in scheduler.tasks if task.due_date == "2026-06-29")
    scheduler.complete_task(task_to_complete)

    assert any(task.due_date == "2026-06-30" for task in scheduler.tasks)
    assert any(task.status == "pending" and task.due_date == "2026-06-30" for task in scheduler.tasks)
