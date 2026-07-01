from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")

    pet1 = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    pet2 = Pet("pet-2", "Luna", "cat", "siamese", 2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    morning_walk = Task(
        "task-1",
        "Morning walk",
        "Take Mochi for a walk",
        "2026-06-29",
        duration_minutes=30,
        priority="high",
        preferred_time="08:00",
    )
    feeding = Task(
        "task-2",
        "Feeding",
        "Feed Luna dinner",
        "2026-06-29",
        duration_minutes=10,
        priority="medium",
        preferred_time="18:00",
    )
    medication = Task(
        "task-3",
        "Medication",
        "Give Mochi medicine",
        "2026-06-29",
        duration_minutes=5,
        priority="high",
        preferred_time="09:00",
    )
    duplicate_time_task = Task(
        "task-5",
        "Lunch prep",
        "Prepare food for Mochi",
        "2026-06-29",
        duration_minutes=15,
        priority="medium",
        preferred_time="08:00",
    )
    bedtime_check = Task(
        "task-4",
        "Bedtime check",
        "Check Luna before bed",
        "2026-06-29",
        duration_minutes=10,
        priority="low",
        preferred_time="21:00",
    )

    medication.mark_complete()

    morning_walk.pet = pet1
    medication.pet = pet1
    duplicate_time_task.pet = pet1
    feeding.pet = pet2
    bedtime_check.pet = pet2

    pet1.add_task(morning_walk)
    pet1.add_task(medication)
    pet1.add_task(duplicate_time_task)
    pet2.add_task(feeding)
    pet2.add_task(bedtime_check)

    scheduler = Scheduler("schedule-1", owner, pet1, "2026-06-29", "2026-06-29")

    # Add tasks out of order to demonstrate sorting.
    scheduler.add_task(bedtime_check)
    scheduler.add_task(morning_walk)
    scheduler.add_task(feeding)
    scheduler.add_task(medication)
    scheduler.add_task(duplicate_time_task)

    scheduler.generate()

    print("Today's Schedule")
    print("----------------")
    for task in scheduler.tasks:
        print(f"- {task.preferred_time or 'TBD'} | {task.title} | Pet: {task.pet.name if task.pet else 'Unassigned'} | Priority: {task.priority} | Status: {task.status} | Duration: {task.duration_minutes} min")

    warning = scheduler.get_conflict_warning()
    if warning:
        print(f"\nConflict warning: {warning}")
    else:
        print("\nNo conflicts detected.")

    print("\nFiltered: pending tasks for Mochi")
    for task in scheduler.filter_tasks_by_status_or_pet(status="pending", pet_name="Mochi"):
        print(f"- {task.title} at {task.preferred_time}")


if __name__ == "__main__":
    main()
