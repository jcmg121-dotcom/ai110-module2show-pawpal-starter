from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    task_id: str
    title: str
    description: str
    due_date: str
    status: str = "pending"

    def complete(self) -> None:
        self.status = "completed"

    def reschedule(self, new_date: str) -> None:
        self.due_date = new_date


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    owner_id: str

    def get_schedule(self) -> Optional["Schedule"]:
        pass


class Owner:
    def __init__(self, owner_id: str, name: str, email: str, phone: str, availability: List[str] = None):
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.availability: List[str] = availability or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass


class Schedule:
    def __init__(self, schedule_id: str, owner_id: str, pet_id: str, start_date: str, end_date: str):
        self.schedule_id = schedule_id
        self.owner_id = owner_id
        self.pet_id = pet_id
        self.start_date = start_date
        self.end_date = end_date
        self.tasks: List[Task] = []

    def generate(self, owner: Owner) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass
