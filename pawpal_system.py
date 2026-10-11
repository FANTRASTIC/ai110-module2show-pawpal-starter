from dataclasses import dataclass, field
from datetime import date, time


@dataclass(eq=False)
class Task:
    description: str
    due_date: date
    due_time: time
    duration_minutes: int = 20
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self):
        pass


@dataclass(eq=False)
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task):
        pass

    def list_tasks(self):
        pass


@dataclass(eq=False)
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet):
        pass

    def get_all_tasks(self):
        pass


@dataclass
class Scheduler:
    owner: Owner

    def get_schedule(self, start_date, end_date=None):
        pass

    def sort_by_time(self, tasks):
        pass

    def filter_tasks(self, tasks, pet=None, completed=None):
        pass

    def detect_conflicts(self, tasks):
        pass

    def mark_task_complete(self, task):
        pass
