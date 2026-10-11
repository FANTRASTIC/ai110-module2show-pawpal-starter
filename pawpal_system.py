from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timedelta


@dataclass(eq=False)
class Task:
    """One scheduled care activity; recurrence advances on completion."""
    description: str
    due_date: date
    due_time: time
    duration_minutes: int = 20
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def __post_init__(self):
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("Task description cannot be blank.")
        if not isinstance(self.due_date, date) or isinstance(self.due_date, datetime):
            raise ValueError("Due date must be a date.")
        if not isinstance(self.due_time, time) or self.due_time.tzinfo is not None:
            raise ValueError("Due time must be a local time without a timezone.")
        if type(self.duration_minutes) is not int or self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive whole number of minutes.")
        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be low, medium, or high.")
        if self.frequency not in ("once", "daily", "weekly"):
            raise ValueError("Frequency must be once, daily, or weekly.")

    def mark_complete(self):
        self.completed = True


@dataclass(eq=False)
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self):
        self.name = self.name.strip()
        self.species = self.species.strip()
        if not self.name or not self.species:
            raise ValueError("Pet name and species cannot be blank.")

    def add_task(self, task):
        if task in self.tasks:
            raise ValueError("This task is already assigned to this pet.")
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks.copy()


@dataclass(eq=False)
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Owner name cannot be blank.")

    def add_pet(self, pet):
        if any(existing.name.casefold() == pet.name.casefold() for existing in self.pets):
            raise ValueError("A pet with this name already exists. Use a distinct name.")
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return (pet, task) pairs so combined schedules retain ownership."""
        return [(pet, task) for pet in self.pets for task in pet.list_tasks()]


@dataclass
class Scheduler:
    owner: Owner

    def get_schedule(self, start_date=None, end_date=None):
        """Return stored tasks in chronological order, optionally within a date range."""
        if end_date is not None and start_date is None:
            raise ValueError("An end date requires a start date.")
        if start_date is not None:
            end_date = end_date or start_date
            if end_date < start_date:
                raise ValueError("End date cannot be before start date.")
        tasks = self.owner.get_all_tasks()
        if start_date is not None:
            tasks = [(pet, task) for pet, task in tasks
                     if start_date <= task.due_date <= end_date]
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks=None):
        tasks = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda entry: (entry[1].due_date, entry[1].due_time))

    def filter_tasks(self, pet_name=None, completed=None, tasks=None):
        tasks = self.owner.get_all_tasks() if tasks is None else tasks
        return [(pet, task) for pet, task in tasks
                if (pet_name is None or pet.name == pet_name)
                and (completed is None or task.completed == completed)]

    def detect_conflicts(self, tasks=None):
        """Warn about pending tasks sharing an exact start date and time."""
        tasks = self.owner.get_all_tasks() if tasks is None else tasks
        slots = {}
        for pet, task in tasks:
            if not task.completed:
                slots.setdefault((task.due_date, task.due_time), []).append((pet, task))
        warnings = []
        for (day, start), entries in sorted(slots.items()):
            if len(entries) > 1:
                descriptions = "; ".join(f"{pet.name}: {task.description}" for pet, task in entries)
                warnings.append(f"Conflict on {day} at {start:%H:%M}: {descriptions}")
        return warnings

    def mark_task_complete(self, task):
        """Complete a stored task once, returning its new recurring occurrence."""
        pet = next((pet for pet, stored in self.owner.get_all_tasks() if stored is task), None)
        if pet is None:
            raise ValueError("Task does not belong to this owner.")
        if task.completed:
            return None
        next_task = None
        if task.frequency != "once":
            days = 1 if task.frequency == "daily" else 7
            next_task = replace(task, due_date=task.due_date + timedelta(days=days), completed=False)
            pet.add_task(next_task)
        task.mark_complete()
        return next_task
