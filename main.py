from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    day = date(2026, 10, 11)
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    mochi.add_task(Task("Evening walk", day, time(18), 30, "high"))
    breakfast = Task("Breakfast", day, time(8), 10, "high", "daily")
    mochi.add_task(breakfast)
    luna.add_task(Task("Medication", day, time(8), 5, "high"))
    luna.add_task(Task("Grooming", day, time(10), 15, "medium", "weekly"))
    scheduler = Scheduler(owner)

    print(f"Today's Schedule (fixed demo date: {day})")
    for pet, task in scheduler.get_schedule(day):
        print(f"  {task.due_time:%H:%M} | {pet.name}: {task.description} "
              f"({task.duration_minutes} min, {task.priority}, {task.frequency})")
    print("\nPending tasks for Luna:")
    for pet, task in scheduler.filter_tasks(pet_name="Luna", completed=False):
        print(f"  {pet.name}: {task.description}")
    print("\nConflict warnings:")
    for warning in scheduler.detect_conflicts():
        print(f"  {warning}")
    next_task = scheduler.mark_task_complete(breakfast)
    print(f"\nCompleted Mochi's {breakfast.description}.")
    print(f"Next occurrence: {next_task.due_date} at {next_task.due_time:%H:%M}; "
          f"completed={next_task.completed}")
    scheduler.mark_task_complete(breakfast)
    print(f"After repeated completion: {len(mochi.tasks)} tasks for Mochi (no duplicate).")


if __name__ == "__main__":
    main()
