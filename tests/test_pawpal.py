from datetime import date, time

from pawpal_system import Pet, Task


def test_mark_complete():
    task = Task("Feed", date(2026, 10, 11), time(8))
    task.mark_complete()
    assert task.completed is True


def test_add_task():
    pet = Pet("Mochi", "dog")
    task = Task("Walk", date(2026, 10, 11), time(9))
    pet.add_task(task)
    assert pet.list_tasks() == [task]
    assert len(pet.tasks) == 1
