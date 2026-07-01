import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app now keeps your owner, pet, and tasks in Streamlit session state so they persist across reruns.
"""
)

if "owner" not in st.session_state or not isinstance(st.session_state.owner, Owner):
    st.session_state.owner = Owner("owner-1", "Jordan", "jordan@example.com", "555-0100")

if "pet" not in st.session_state or not isinstance(st.session_state.pet, Pet):
    st.session_state.pet = Pet("pet-1", "Mochi", "dog", "mixed", 3)
    if st.session_state.pet not in st.session_state.owner.pets:
        st.session_state.owner.add_pet(st.session_state.pet)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

owner = st.session_state.owner
pet = st.session_state.pet

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

pet_name = st.text_input("Pet name", value=pet.name)
if pet_name != pet.name:
    pet.name = pet_name

species_options = ["dog", "cat", "other"]
species_index = species_options.index(pet.species) if pet.species in species_options else 0
species = st.selectbox("Species", species_options, index=species_index)
if species != pet.species:
    pet.species = species

if st.button("Add pet"):
    new_pet = Pet(f"pet-{len(owner.pets) + 1}", pet_name, species, "mixed", 3)
    owner.add_pet(new_pet)
    st.session_state.pet = new_pet
    st.session_state.owner = owner
    st.success(f"Added {new_pet.name} to {owner.name}'s pets.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These are stored in session state and used to build the schedule.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    recurring_interval_days = st.number_input("Repeat every X days", min_value=0, max_value=30, value=0)

if st.button("Add task"):
    task = Task(
        task_id=f"task-{len(st.session_state.tasks) + 1}",
        title=task_title,
        description=f"{task_title} for {pet.name}",
        due_date="2026-06-29",
        duration_minutes=int(duration),
        priority=priority,
        preferred_time="08:00",
        recurring_interval_days=int(recurring_interval_days),
    )
    pet.add_task(task)
    st.session_state.tasks.append(task)
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler("schedule-1", owner, pet, "2026-06-29", "2026-06-29")
    else:
        st.session_state.scheduler.add_task(task)

if st.session_state.tasks:
    st.success("Current tasks are previewed in scheduler order.")
    preview_scheduler = Scheduler("preview-schedule", owner, pet, "2026-06-29", "2026-06-29")
    for task in st.session_state.tasks:
        preview_scheduler.add_task(task)

    sorted_tasks = preview_scheduler.sort_tasks()
    task_rows = [
        {
            "Task": task.title,
            "Time": task.preferred_time or "TBD",
            "Priority": task.priority.title(),
            "Duration (min)": task.duration_minutes,
        }
        for task in sorted_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler("schedule-1", owner, pet, "2026-06-29", "2026-06-29")
    for task in st.session_state.tasks:
        scheduler.add_task(task)
    scheduler.generate()
    st.session_state.scheduler = scheduler

if "scheduler" in st.session_state:
    st.success("Schedule generated successfully.")

    pet_options = ["All"] + [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Filter by pet", pet_options)
    selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None) if selected_pet_name != "All" else None
    status_options = ["All", "pending", "completed"]
    selected_status = st.selectbox("Filter by status", status_options)
    status_filter = None if selected_status == "All" else selected_status

    visible_tasks = st.session_state.scheduler.filter_tasks(pet=selected_pet, status=status_filter)
    if visible_tasks:
        st.success(f"Showing {len(visible_tasks)} tasks in sorted order.")
        table_rows = [
            {
                "Time": task.preferred_time or "TBD",
                "Task": task.title,
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Priority": task.priority.title(),
                "Status": task.status.title(),
                "Duration (min)": task.duration_minutes,
            }
            for task in visible_tasks
        ]
        st.table(table_rows)
    else:
        st.info("No tasks match the selected filters.")

    conflict_warning = st.session_state.scheduler.get_conflict_warning()
    if conflict_warning:
        st.warning(conflict_warning)
    else:
        st.success("No scheduling conflicts detected.")
