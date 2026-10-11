from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Manage your pets, schedule care activities, and view your daily plan.")
st.caption("Changes stay in this browser session. They are not saved after the session ends.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)

with st.expander("Owner details"):
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value=owner.name)
        if st.form_submit_button("Save owner"):
            if owner_name.strip():
                owner.name = owner_name.strip()
                st.success("Owner details saved.")
            else:
                st.error("Owner name cannot be blank.")
st.write(f"Owner: {owner.name}")

st.subheader("Pets")
with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        try:
            owner.add_pet(Pet(pet_name, species))
            st.success(f"Added {pet_name.strip()}.")
        except ValueError as error:
            st.error(str(error))

if not owner.pets:
    st.info("Add a pet to start scheduling care.")
    st.stop()
st.table([{"Pet": pet.name, "Species": pet.species, "Stored tasks": len(pet.tasks)}
          for pet in owner.pets])

st.subheader("Tasks")
with st.form("task_form"):
    selected_pet = st.selectbox("Pet for task", [pet.name for pet in owner.pets])
    task_title = st.text_input("Task title", value="Morning walk")
    day = st.date_input("Due date", value=date.today())
    due_time = st.time_input("Due time", value=time(8))
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    if st.form_submit_button("Add task"):
        try:
            task = Task(task_title, day, due_time, int(duration), priority, frequency)
            pet = next(pet for pet in owner.pets if pet.name == selected_pet)
            pet.add_task(task)
            st.success(f"Added {task.description} for {pet.name}.")
        except ValueError as error:
            st.error(str(error))

pending = scheduler.filter_tasks(completed=False)
if pending:
    with st.expander("Edit a pending task"):
        selected_index = st.selectbox(
            "Task to edit", range(len(pending)),
            format_func=lambda index: (
                f"{pending[index][0].name}: {pending[index][1].description} "
                f"({pending[index][1].due_date} {pending[index][1].due_time:%H:%M})"
            ),
        )
        pet, original = pending[selected_index]
        with st.form(f"edit_task_{id(original)}"):
            title = st.text_input("New title", value=original.description)
            new_day = st.date_input("New due date", value=original.due_date)
            new_time = st.time_input("New due time", value=original.due_time)
            minutes = st.number_input("New duration", min_value=1, value=original.duration_minutes)
            new_priority = st.selectbox(
                "New priority", ["low", "medium", "high"],
                index=["low", "medium", "high"].index(original.priority),
            )
            new_frequency = st.selectbox(
                "New frequency", ["once", "daily", "weekly"],
                index=["once", "daily", "weekly"].index(original.frequency),
            )
            if st.form_submit_button("Save task"):
                try:
                    updated = Task(title, new_day, new_time, int(minutes), new_priority, new_frequency)
                    pet.tasks[pet.tasks.index(original)] = updated
                    st.success("Task updated.")
                except ValueError as error:
                    st.error(str(error))

st.divider()
st.subheader("Build Schedule")
schedule_day = st.date_input("Schedule date", value=date.today())
show_all = st.checkbox("Show all stored dates")
pet_filter = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in owner.pets])
status_filter = st.selectbox("Completion status", ["All", "Pending", "Completed"])
if st.button("Generate schedule"):
    st.session_state.show_schedule = True

if st.session_state.get("show_schedule", False):
    schedule = scheduler.get_schedule() if show_all else scheduler.get_schedule(schedule_day)
    for warning in scheduler.detect_conflicts(schedule):
        st.warning(warning)
    completed = {"All": None, "Pending": False, "Completed": True}[status_filter]
    visible = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All pets" else pet_filter,
        completed=completed, tasks=schedule,
    )
    st.caption("Tasks keep their chosen times and are sorted by date, then time. "
               "Priority is shown for your judgment; conflicts flag equal start times. "
               "Complete a daily or weekly task to create its next occurrence.")
    if not visible:
        st.info("No tasks match this schedule and these filters.")
    else:
        st.table([{
            "Date": str(task.due_date), "Time": task.due_time.strftime("%H:%M"),
            "Pet": pet.name, "Task": task.description, "Minutes": task.duration_minutes,
            "Priority": task.priority, "Frequency": task.frequency,
            "Status": "Completed" if task.completed else "Pending",
        } for pet, task in visible])
        for pet, task in visible:
            if not task.completed and st.button(
                f"Complete {pet.name}: {task.description} ({task.due_date} {task.due_time:%H:%M})",
                key=f"complete_{id(task)}",
            ):
                try:
                    next_task = scheduler.mark_task_complete(task)
                    st.session_state.completion_message = (
                        f"Completed {task.description} for {pet.name}."
                        + (f" Next occurrence: {next_task.due_date}." if next_task else "")
                    )
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    if "completion_message" in st.session_state:
        st.success(st.session_state.pop("completion_message"))
