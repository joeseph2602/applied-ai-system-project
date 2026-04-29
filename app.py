import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Investigate st.session_state and check for existing owner object
st.markdown("### Session State Investigation")
with st.expander("Session State Debug Info", expanded=False):
    st.write("Current session state keys:", list(st.session_state.keys()))

    # Check if owner object exists in session state
    if "owner" not in st.session_state:
        st.info("❌ No 'owner' object found in session state. Will create new one.")
        owner_created = False
    else:
        st.success("✅ 'owner' object exists in session state!")
        owner_created = True
        st.write("Owner details:", st.session_state.owner.view_details() if hasattr(st.session_state.owner, 'view_details') else str(st.session_state.owner))

# Create or retrieve owner object
if "owner" not in st.session_state:
    # Create new owner object
    st.session_state.owner = Owner(
        id=1,
        name=owner_name,
        email=f"{owner_name.lower()}@example.com"
    )
    st.success(f"🆕 Created new owner: {st.session_state.owner.name}")
else:
    # Update existing owner name if changed
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name
        st.info(f"📝 Updated owner name to: {owner_name}")

st.markdown("### Tasks")
st.caption("Add tasks to specific pets using the PawPal system methods.")

# Only show task form if there are pets
if not st.session_state.owner.pets:
    st.warning("⚠️ Add at least one pet first before creating tasks.")
else:
    # Select which pet to add task to
    pet_options = [f"{pet.name} ({pet.species})" for pet in st.session_state.owner.pets]
    selected_pet_index = st.selectbox("Select pet for task", range(len(pet_options)), format_func=lambda x: pet_options[x])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk", key="task_desc")
    with col2:
        task_time = st.text_input("Time (e.g., 8:00 AM)", value="8:00 AM", key="task_time")
    with col3:
        task_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "One-time"], key="task_freq")

    if st.button("Add Task to Pet"):
        if task_description.strip() and task_time.strip():
            selected_pet = st.session_state.owner.pets[selected_pet_index]

            # Generate unique task ID
            existing_task_ids = [t.id for t in st.session_state.owner.get_all_tasks()]
            task_id = max(existing_task_ids) + 1 if existing_task_ids else 1

            # Create new Task object using PawPal system
            new_task = Task(
                id=task_id,
                description=task_description,
                time=task_time,
                frequency=task_frequency
            )

            # Add task to selected pet using the method
            selected_pet.add_task(new_task)

            st.success(f"✅ Added task '{task_description}' to {selected_pet.name}!")
            st.rerun()
        else:
            st.error("Please enter both task description and time.")

# Display all tasks from all pets
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("**All Tasks:**")
    task_data = []
    for task in all_tasks:
        # Find which pet this task belongs to
        pet_name = "Unknown"
        for pet in st.session_state.owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break

        task_data.append({
            "Pet": pet_name,
            "Description": task.description,
            "Time": task.time,
            "Frequency": task.frequency,
            "Status": task.status.value
        })

    st.table(task_data)
else:
    st.info("No tasks added yet.")

st.markdown("### Owner's Pets")
st.caption("Manage pets for the current owner.")

# Display current pets
if st.session_state.owner.pets:
    st.write("Current pets:")
    for pet in st.session_state.owner.pets:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{pet.name}** ({pet.species})")
            with col2:
                st.write(f"Age: {pet.age}")
            with col3:
                st.write(f"Health: {pet.health.value}")
else:
    st.info("No pets added yet.")

# Add new pet form
with st.expander("Add New Pet", expanded=False):
    new_pet_name = st.text_input("Pet name", key="new_pet_name")
    new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Other"], key="new_pet_species")
    new_pet_age = st.number_input("Age", min_value=0, max_value=30, value=1, key="new_pet_age")
    new_pet_weight = st.number_input("Weight (lbs)", min_value=0.1, max_value=200.0, value=10.0, key="new_pet_weight")

    if st.button("Add Pet"):
        if new_pet_name.strip():
            # Create new pet
            pet_id = len(st.session_state.owner.pets) + 1
            new_pet = Pet(
                id=pet_id,
                name=new_pet_name,
                species=new_pet_species,
                age=new_pet_age,
                weight=new_pet_weight
            )

            # Add to owner
            st.session_state.owner.add_pet(new_pet)
            st.success(f"🐾 Added {new_pet.name} to {st.session_state.owner.name}'s pets!")
            st.rerun()
        else:
            st.error("Please enter a pet name.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using the PawPal Scheduler class.")

# Show current owner and pets summary
if st.session_state.owner.pets:
    st.info(f"📊 Ready to schedule for {st.session_state.owner.name} with {len(st.session_state.owner.pets)} pet(s)")
else:
    st.warning("⚠️ Add some pets first before generating a schedule")

if st.button("Generate Schedule"):
    if not st.session_state.owner.pets:
        st.error("Please add at least one pet before generating a schedule.")
    elif total_tasks == 0:
        st.error("Please add at least one task before generating a schedule.")
    else:
        # Create Scheduler instance and generate schedule
        scheduler = Scheduler(owner=st.session_state.owner)

        # Get all tasks using Scheduler method
        all_tasks = scheduler.get_all_tasks()
        pending_tasks = scheduler.get_pending_tasks()

        st.success("🎯 Schedule Generated Successfully!")
        st.markdown("### Today's Schedule")

        if pending_tasks:
            st.write(f"**Pending Tasks ({len(pending_tasks)}):**")
            for task in pending_tasks:
                # Find pet name for this task
                pet_name = "Unknown"
                for pet in st.session_state.owner.pets:
                    if task in pet.tasks:
                        pet_name = pet.name
                        break

                st.write(f"- **{task.time}** - {task.description} for {pet_name} ({task.frequency})")
        else:
            st.info("All tasks are completed! 🎉")

        # Show summary stats
        st.markdown("### Schedule Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", total_tasks)
        with col2:
            st.metric("Pending Tasks", len(pending_tasks))
        with col3:
            st.metric("Completed Tasks", total_tasks - len(pending_tasks))

        # Option to mark tasks complete
        if pending_tasks:
            st.markdown("### Mark Tasks Complete")
            task_options = [f"{t.time} - {t.description}" for t in pending_tasks]
            selected_task_index = st.selectbox("Select task to mark complete", range(len(task_options)),
                                             format_func=lambda x: task_options[x])

            if st.button("Mark Selected Task Complete"):
                selected_task = pending_tasks[selected_task_index]
                success = scheduler.mark_task_complete(selected_task.id)
                if success:
                    st.success(f"✅ Marked '{selected_task.description}' as complete!")
                    st.rerun()
                else:
                    st.error("Failed to mark task complete.")
