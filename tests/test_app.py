from datetime import date, time
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def widget(app, kind, label):
    return next(item for item in getattr(app, kind) if item.label == label)


def test_ui_multi_pet_schedule_filters_completion_and_persistence():
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    widget(app, "text_input", "Pet name").set_value("Mochi")
    widget(app, "button", "Add pet").click().run()
    widget(app, "text_input", "Pet name").set_value("Luna")
    widget(app, "selectbox", "Species").select("cat")
    widget(app, "button", "Add pet").click().run()
    day = date(2026, 10, 11)
    for pet_name, title, start, frequency in [
        ("Mochi", "Evening walk", time(18), "once"),
        ("Mochi", "Breakfast", time(8), "daily"),
        ("Luna", "Medication", time(8), "once"),
    ]:
        widget(app, "selectbox", "Pet for task").select(pet_name)
        widget(app, "text_input", "Task title").set_value(title)
        widget(app, "date_input", "Due date").set_value(day)
        widget(app, "time_input", "Due time").set_value(start)
        widget(app, "selectbox", "Frequency").select(frequency)
        widget(app, "button", "Add task").click().run()
    widget(app, "date_input", "Schedule date").set_value(day)
    widget(app, "button", "Generate schedule").click().run()
    assert not app.exception
    schedule = app.table[-1].value
    assert list(schedule["Task"]) == ["Breakfast", "Medication", "Evening walk"]
    assert "Mochi: Breakfast; Luna: Medication" in app.warning[0].value
    widget(app, "selectbox", "Filter by pet").select("Luna").run()
    assert list(app.table[-1].value["Pet"]) == ["Luna"]
    widget(app, "selectbox", "Filter by pet").select("All pets").run()
    widget(app, "button", "Complete Mochi: Breakfast (2026-10-11 08:00)").click().run()
    widget(app, "checkbox", "Show all stored dates").check().run()
    schedule = app.table[-1].value
    assert list(schedule["Status"]) == ["Completed", "Pending", "Pending", "Pending"]
    assert list(schedule["Date"])[-1] == "2026-10-12"
    assert not app.warning
    widget(app, "selectbox", "Completion status").select("Completed").run()
    assert list(app.table[-1].value["Task"]) == ["Breakfast"]
    app.run()
    owner = app.session_state["owner"]
    assert len(owner.pets) == 2
    assert len(owner.pets[0].tasks) == 3
    assert owner.pets[0].tasks[1].completed
    assert not app.exception


def test_ui_validation_and_editing_preserve_existing_data():
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    widget(app, "text_input", "Pet name").set_value(" ")
    widget(app, "button", "Add pet").click().run()
    assert "cannot be blank" in app.error[0].value
    widget(app, "text_input", "Pet name").set_value("Mochi")
    widget(app, "button", "Add pet").click().run()
    widget(app, "text_input", "Pet name").set_value("mochi")
    widget(app, "button", "Add pet").click().run()
    assert "already exists" in app.error[0].value
    widget(app, "text_input", "Task title").set_value(" ")
    widget(app, "button", "Add task").click().run()
    assert "cannot be blank" in app.error[0].value
    assert app.session_state["owner"].pets[0].tasks == []
    widget(app, "text_input", "Task title").set_value("Walk")
    widget(app, "button", "Add task").click().run()
    widget(app, "text_input", "New title").set_value("Evening walk")
    widget(app, "number_input", "New duration").set_value(30)
    widget(app, "button", "Save task").click().run()
    task = app.session_state["owner"].pets[0].tasks[0]
    assert (task.description, task.duration_minutes) == ("Evening walk", 30)
    widget(app, "text_input", "New title").set_value(" ")
    widget(app, "button", "Save task").click().run()
    assert "cannot be blank" in app.error[0].value
    assert app.session_state["owner"].pets[0].tasks[0] is task
    assert not app.exception
