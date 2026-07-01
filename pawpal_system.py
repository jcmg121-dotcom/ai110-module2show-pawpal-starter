from copy import deepcopy
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Tuple


@dataclass
class Task:
    task_id: str
    title: str
    description: str
    due_date: str
    status: str = "pending"
    duration_minutes: int = 15
    priority: str = "medium"
    preferred_time: Optional[str] = None
    scheduler: Optional["Scheduler"] = None
    pet: Optional["Pet"] = None
    recurring_interval_days: int = 0

    def complete(self) -> None:
        """Mark the task as completed and create the next recurring occurrence when needed."""
        if self.scheduler is not None:
            self.scheduler.complete_task(self)
        else:
            self.mark_complete()

    def mark_complete(self) -> None:
        """Update the task status to completed."""
        self.status = "completed"

    def create_next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence of a recurring task if applicable."""
        if not self.recurring_interval_days or self.recurring_interval_days <= 0:
            return None

        current_date = date.fromisoformat(self.due_date)
        next_date = current_date + timedelta(days=self.recurring_interval_days)
        next_task = deepcopy(self)
        next_task.status = "pending"
        next_task.due_date = next_date.strftime("%Y-%m-%d")
        next_task.task_id = f"{self.task_id}-next"
        next_task.scheduler = None
        next_task.pet = self.pet
        return next_task

    def reschedule(self, new_date: str) -> None:
        """Move the task to a new due date."""
        self.due_date = new_date

    def sort_key(self) -> Tuple[int, int, str]:
        """Create a sort key that considers priority, time, and due date."""
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        time_value = self._time_to_minutes(self.preferred_time or "23:59")
        return (
            priority_rank.get(self.priority.lower(), 1),
            time_value,
            self.due_date,
        )

    @staticmethod
    def _time_to_minutes(time_value: str) -> int:
        """Convert an HH:MM string into minutes since midnight."""
        hour_str, minute_str = time_value.split(":")
        return int(hour_str) * 60 + int(minute_str)


class Pet:
    def __init__(self, pet_id: str, name: str, species: str, breed: str, age: int):
        """Initialize a pet profile with core identity and care details."""
        self.pet_id = pet_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner: Optional["Owner"] = None
        self.schedule: Optional["Scheduler"] = None
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def get_schedule(self) -> Optional["Scheduler"]:
        """Return the pet's current schedule, if one exists."""
        return self.schedule


class Owner:
    def __init__(self, owner_id: str, name: str, email: str, phone: str, availability: Optional[List[str]] = None):
        """Initialize an owner profile and the list of pets they manage."""
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.availability: List[str] = availability or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by pet ID."""
        remaining_pets: List[Pet] = []
        for pet in self.pets:
            if pet.pet_id != pet_id:
                remaining_pets.append(pet)
            else:
                pet.owner = None
        self.pets = remaining_pets


class Scheduler:
    def __init__(self, schedule_id: str, owner: Owner, pet: Pet, start_date: str, end_date: str):
        """Initialize a scheduler for a specific owner, pet, and date range."""
        self.schedule_id = schedule_id
        self.owner = owner
        self.pet = pet
        self.start_date = start_date
        self.end_date = end_date
        self.tasks: List[Task] = []

        if owner is not None and pet not in owner.pets:
            owner.add_pet(pet)
        if pet is not None:
            pet.schedule = self

    def generate(self) -> None:
        """Expand recurring tasks and sort them by priority, date, and time."""
        expanded_tasks: List[Task] = []
        start_date = date.fromisoformat(self.start_date)
        end_date = date.fromisoformat(self.end_date)

        for task in self.tasks:
            if task.recurring_interval_days and task.recurring_interval_days > 0:
                occurrence_date = start_date
                occurrence_index = 1
                while occurrence_date <= end_date:
                    recurring_task = deepcopy(task)
                    recurring_task.task_id = f"{task.task_id}-{occurrence_index}"
                    recurring_task.due_date = occurrence_date.strftime("%Y-%m-%d")
                    recurring_task.scheduler = self
                    if recurring_task.pet is None:
                        recurring_task.pet = self.pet
                    expanded_tasks.append(recurring_task)
                    occurrence_index += 1
                    occurrence_date += timedelta(days=task.recurring_interval_days)
            else:
                task.scheduler = self
                if task.pet is None:
                    task.pet = self.pet
                expanded_tasks.append(task)

        self.tasks = self.sort_tasks(expanded_tasks)

    def add_task(self, task: Task) -> None:
        """Add a task to this scheduler."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.scheduler = self
            if task.pet is None:
                task.pet = self.pet

    def complete_task(self, task: Task) -> None:
        """Mark a task complete and create the next recurring occurrence if needed."""
        task.mark_complete()
        next_occurrence = task.create_next_occurrence()
        if next_occurrence is not None:
            next_occurrence.scheduler = self
            if next_occurrence not in self.tasks and not any(
                existing.due_date == next_occurrence.due_date and existing.title == next_occurrence.title
                for existing in self.tasks
            ):
                self.add_task(next_occurrence)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this scheduler by task ID."""
        remaining_tasks: List[Task] = []
        for task in self.tasks:
            if task.task_id != task_id:
                remaining_tasks.append(task)
            else:
                task.scheduler = None
        self.tasks = remaining_tasks

    def filter_tasks(self, pet: Optional[Pet] = None, status: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by pet and/or status."""
        filtered_tasks = list(self.tasks)
        if pet is not None:
            filtered_tasks = [task for task in filtered_tasks if task.pet is pet]
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.status.lower() == status.lower()]
        return self.sort_tasks(filtered_tasks)

    def filter_tasks_by_status_or_pet(self, status: Optional[str] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered_tasks = list(self.tasks)

        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.status.lower() == status.lower()]

        if pet_name is not None:
            filtered_tasks = [task for task in filtered_tasks if task.pet is not None and task.pet.name.lower() == pet_name.lower()]

        return self.sort_tasks(filtered_tasks)

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of pending tasks that share the same date and preferred time."""
        pending_tasks = [task for task in self.tasks if task.status.lower() == "pending"]
        conflicts: List[Tuple[Task, Task]] = []

        for index, first_task in enumerate(pending_tasks):
            for second_task in pending_tasks[index + 1 :]:
                if (
                    first_task.due_date == second_task.due_date
                    and first_task.preferred_time
                    and second_task.preferred_time
                    and first_task.preferred_time == second_task.preferred_time
                ):
                    conflicts.append((first_task, second_task))

        return conflicts

    def get_conflict_warning(self) -> Optional[str]:
        """Return a lightweight warning message for scheduling conflicts, if any."""
        conflicts = self.detect_conflicts()
        if not conflicts:
            return None

        conflict_lines = [
            f"{first.title} and {second.title} overlap at {first.preferred_time} on {first.due_date}"
            for first, second in conflicts
        ]
        return "Warning: " + "; ".join(conflict_lines)

    def sort_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by priority, time, and due date."""
        task_list = list(tasks if tasks is not None else self.tasks)
        return sorted(task_list, key=lambda task: task.sort_key())
