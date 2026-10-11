from datetime import date, time

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


DAY = date(2026, 10, 11)


@pytest.fixture
def household():
    owner = Owner("Jordan")
    dog, cat = Pet("Mochi", "dog"), Pet("Luna", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat, Scheduler(owner)


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


def test_multi_pet_retrieval_retains_ownership(household):
    owner, dog, cat, scheduler = household
    walk = Task("Walk", DAY, time(9))
    feed = Task("Feed", DAY, time(8))
    dog.add_task(walk)
    cat.add_task(feed)
    assert owner.get_all_tasks() == [(dog, walk), (cat, feed)]
    assert scheduler.get_schedule() == [(cat, feed), (dog, walk)]


def test_sort_dates_before_times_and_keep_ties_stable(household):
    _, dog, cat, scheduler = household
    tomorrow = Task("Tomorrow", date(2026, 10, 12), time(7))
    evening = Task("Evening", DAY, time(18))
    same_time = Task("Evening medication", DAY, time(18))
    dog.add_task(tomorrow)
    dog.add_task(evening)
    cat.add_task(same_time)
    original = [(dog, tomorrow), (dog, evening), (cat, same_time)]
    assert scheduler.sort_by_time(original) == [(dog, evening), (cat, same_time), (dog, tomorrow)]
    assert original[0] == (dog, tomorrow)


def test_filter_by_pet_name(household):
    _, dog, cat, scheduler = household
    walk, feed = Task("Walk", DAY, time(9)), Task("Feed", DAY, time(8))
    dog.add_task(walk)
    cat.add_task(feed)
    assert scheduler.filter_tasks(pet_name="Luna") == [(cat, feed)]
    assert scheduler.filter_tasks(pet_name="Unknown") == []


def test_filter_completion_across_pets_and_combined_criteria(household):
    _, dog, cat, scheduler = household
    done = Task("Walk", DAY, time(9), completed=True)
    pending = Task("Feed", DAY, time(8))
    dog.add_task(done)
    cat.add_task(pending)
    assert scheduler.filter_tasks(completed=True) == [(dog, done)]
    assert scheduler.filter_tasks(completed=False) == [(cat, pending)]
    assert scheduler.filter_tasks(pet_name="Mochi", completed=False) == []
    assert scheduler.filter_tasks(pet_name="Luna", completed=False) == [(cat, pending)]


@pytest.mark.parametrize("frequency, expected", [
    ("daily", date(2027, 1, 1)), ("weekly", date(2027, 1, 7)),
])
def test_recurrence_preserves_details_and_handles_year_boundary(household, frequency, expected):
    _, dog, _, scheduler = household
    task = Task("Medication", date(2026, 12, 31), time(8, 30), 5, "high", frequency)
    dog.add_task(task)
    next_task = scheduler.mark_task_complete(task)
    assert task.completed is True
    assert next_task is not task
    assert next_task.due_date == expected
    assert next_task.completed is False
    assert (next_task.description, next_task.due_time, next_task.duration_minutes,
            next_task.priority, next_task.frequency) == ("Medication", time(8, 30), 5, "high", frequency)
    assert dog.tasks == [task, next_task]


def test_repeated_completion_does_not_duplicate_recurrence(household):
    _, dog, _, scheduler = household
    task = Task("Feed", DAY, time(8), frequency="daily")
    dog.add_task(task)
    first = scheduler.mark_task_complete(task)
    assert scheduler.mark_task_complete(task) is None
    assert dog.tasks == [task, first]
    second = scheduler.mark_task_complete(first)
    assert second.due_date == date(2026, 10, 13)
    assert len(dog.tasks) == 3


def test_once_task_creates_no_recurrence(household):
    _, dog, _, scheduler = household
    task = Task("Vet", DAY, time(8))
    dog.add_task(task)
    assert scheduler.mark_task_complete(task) is None
    assert task.completed
    assert len(dog.tasks) == 1


def test_conflicts_identify_tasks_and_pets(household):
    _, dog, cat, scheduler = household
    dog.add_task(Task("Walk", DAY, time(8)))
    cat.add_task(Task("Feed", DAY, time(8)))
    cat.add_task(Task("Medication", DAY, time(8)))
    assert scheduler.detect_conflicts() == [
        "Conflict on 2026-10-11 at 08:00: Mochi: Walk; Luna: Feed; Luna: Medication"
    ]


def test_conflicts_ignore_completed_different_dates_and_nonidentical_starts(household):
    _, dog, cat, scheduler = household
    dog.add_task(Task("Walk", DAY, time(8), 30))
    cat.add_task(Task("Done", DAY, time(8), completed=True))
    cat.add_task(Task("Tomorrow", date(2026, 10, 12), time(8)))
    cat.add_task(Task("Overlapping but different start", DAY, time(8, 15)))
    assert scheduler.detect_conflicts() == []


def test_empty_collections():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    assert owner.get_all_tasks() == []
    assert scheduler.get_schedule() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
    owner.add_pet(Pet("Mochi", "dog"))
    assert scheduler.get_schedule(DAY) == []


def test_date_range_is_inclusive(household):
    _, dog, _, scheduler = household
    first = Task("First", DAY, time(8))
    last = Task("Last", date(2026, 10, 12), time(8))
    dog.add_task(first)
    dog.add_task(last)
    dog.add_task(Task("Outside", date(2026, 10, 13), time(8)))
    assert scheduler.get_schedule(DAY) == [(dog, first)]
    assert scheduler.get_schedule(DAY, date(2026, 10, 12)) == [(dog, first), (dog, last)]
    with pytest.raises(ValueError, match="before"):
        scheduler.get_schedule(DAY, date(2026, 10, 10))


def test_foreign_task_cannot_be_completed(household):
    _, _, _, scheduler = household
    task = Task("Foreign", DAY, time(8), frequency="daily")
    with pytest.raises(ValueError, match="does not belong"):
        scheduler.mark_task_complete(task)
    assert not task.completed


def test_collections_are_independent_and_list_tasks_is_a_copy():
    first, second = Pet("Mochi", "dog"), Pet("Luna", "cat")
    first.add_task(Task("Walk", DAY, time(8)))
    first.list_tasks().clear()
    assert len(first.tasks) == 1
    assert second.tasks == []
    first_owner, second_owner = Owner("Jordan"), Owner("Alex")
    first_owner.add_pet(first)
    assert second_owner.pets == []


@pytest.mark.parametrize("changes", [
    {"description": "  "}, {"duration_minutes": 0}, {"duration_minutes": 2.5},
    {"priority": "urgent"}, {"frequency": "monthly"}, {"due_date": "2026-10-11"},
    {"due_time": "08:00"},
])
def test_invalid_task_inputs(changes):
    values = {"description": "Feed", "due_date": DAY, "due_time": time(8)}
    values.update(changes)
    with pytest.raises(ValueError):
        Task(**values)


def test_blank_names_and_duplicate_pet_names(household):
    owner, _, _, _ = household
    with pytest.raises(ValueError):
        Owner(" ")
    with pytest.raises(ValueError):
        Pet(" ", "dog")
    with pytest.raises(ValueError, match="already exists"):
        owner.add_pet(Pet(" mochi ", "dog"))
