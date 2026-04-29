from pawpal_system import Owner, Pet, Task, Scheduler, TaskStatus

# Create owner
owner = Owner(id=1, name="Joeseph", email="joe@email.com")

# Create pets
pet1 = Pet(id=1, name="Buddy", species="Dog", age=3, weight=25.0)
pet2 = Pet(id=2, name="Milo", species="Cat", age=2, weight=10.0)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create tasks OUT OF ORDER to test sorting
task1 = Task(id=1, description="Morning Walk", time="8:00 AM", frequency="Daily")
task2 = Task(id=2, description="Feed", time="12:00 PM", frequency="Daily")
task3 = Task(id=3, description="Vet Visit", time="3:00 PM", frequency="One-time")
task4 = Task(id=4, description="Evening Walk", time="6:00 PM", frequency="Daily")
task5 = Task(id=5, description="Play Time", time="10:00 AM", frequency="Daily")
task6 = Task(id=6, description="Brush Fur", time="7:00 AM", frequency="Weekly")
# Add conflicting tasks - same pet at same time
task7 = Task(id=7, description="Morning Grooming", time="8:00 AM", frequency="Weekly")  # Conflicts with task1 for Buddy
# Add conflicting tasks - different pets at same time
task8 = Task(id=8, description="Afternoon Nap", time="2:00 PM", frequency="Daily")  # Milo at 2:00 PM
task9 = Task(id=9, description="Training Session", time="2:00 PM", frequency="Daily")  # Buddy at 2:00 PM

# Assign tasks to pets
pet1.add_task(task1)  # 8:00 AM
pet1.add_task(task4)  # 6:00 PM
pet1.add_task(task5)  # 10:00 AM
pet1.add_task(task7)  # 8:00 AM - CONFLICT with task1
pet1.add_task(task9)  # 2:00 PM
pet2.add_task(task2)  # 12:00 PM
pet2.add_task(task3)  # 3:00 PM
pet2.add_task(task6)  # 7:00 AM
pet2.add_task(task8)  # 2:00 PM - CONFLICT with task9 (different pets)

# Create scheduler
scheduler = Scheduler(owner)

print("=== PawPal Task Management Demo ===\n")

# Test 1: Show unsorted tasks (as added)
print("1. UNSORTED TASKS (as added):")
for task in scheduler.get_all_tasks():
    pet_name = "Unknown"
    for pet in owner.pets:
        if task in pet.tasks:
            pet_name = pet.name
            break
    print(f"   {task.time} - {task.description} for {pet_name}")

print()

# Test 2: Show sorted tasks
print("2. SORTED TASKS (by time):")
sorted_tasks = scheduler.sort_by_time()
for task in sorted_tasks:
    pet_name = "Unknown"
    for pet in owner.pets:
        if task in pet.tasks:
            pet_name = pet.name
            break
    print(f"   {task.time} - {task.description} for {pet_name}")

print()

# Test 2.5: Check for scheduling conflicts
print("2.5. CONFLICT DETECTION:")
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("   🚨 Scheduling conflicts detected:")
    for warning in conflicts:
        print(f"   {warning}")
else:
    print("   ✅ No scheduling conflicts detected!")

print()

# Test 3: Filter by status (all are pending by default)
print("3. FILTER BY STATUS - PENDING TASKS:")
pending_tasks = scheduler.filter_tasks(status=TaskStatus.PENDING)
for task in pending_tasks:
    pet_name = "Unknown"
    for pet in owner.pets:
        if task in pet.tasks:
            pet_name = pet.name
            break
    print(f"   {task.time} - {task.description} for {pet_name} ({task.status.value})")

print()

# Test 4: Filter by pet name
print("4. FILTER BY PET NAME - BUDDY'S TASKS:")
buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
for task in buddy_tasks:
    print(f"   {task.time} - {task.description} ({task.status.value})")

print()

# Test 5: Filter by both status and pet name
print("5. FILTER BY PET NAME - MILO'S TASKS:")
milo_tasks = scheduler.filter_tasks(pet_name="Milo")
for task in milo_tasks:
    print(f"   {task.time} - {task.description} ({task.status.value})")

print()

# Test 6: Mark a task complete and show filtering
print("6. MARK TASK COMPLETE AND FILTER:")
scheduler.mark_task_complete(task1.id)  # Mark "Morning Walk" complete
completed_tasks = scheduler.filter_tasks(status=TaskStatus.COMPLETED)
print(f"   Completed tasks: {len(completed_tasks)}")
for task in completed_tasks:
    pet_name = "Unknown"
    for pet in owner.pets:
        if task in pet.tasks:
            pet_name = pet.name
            break
    print(f"   ✓ {task.time} - {task.description} for {pet_name}")

print()
print("=== Demo Complete ===")