import pytest
from datetime import datetime
from pawpal_system import Pet, Task, Owner, Scheduler, HealthStatus, TaskStatus


class TestPet:
    """Test cases for the Pet class."""

    def test_pet_creation_and_view_details(self):
        """Test creating a pet and viewing its details."""
        # Create a pet
        pet = Pet(
            id=1,
            name="Buddy",
            species="Dog",
            age=3,
            weight=25.5,
            health=HealthStatus.GOOD
        )

        # Verify pet attributes
        assert pet.id == 1
        assert pet.name == "Buddy"
        assert pet.species == "Dog"
        assert pet.age == 3
        assert pet.weight == 25.5
        assert pet.health == HealthStatus.GOOD

        # Test view_details method
        details = pet.view_details()
        assert details["name"] == "Buddy"
        assert details["species"] == "Dog"
        assert details["age"] == 3
        assert details["weight"] == 25.5
        assert details["health"] == "Good"
        assert details["task_count"] == 0

    def test_pet_validation(self):
        """Test that pet validation works correctly."""
        # Test negative age raises error
        with pytest.raises(ValueError, match="Age cannot be negative"):
            Pet(id=1, name="Test", species="Dog", age=-1, weight=10.0)

        # Test zero weight raises error
        with pytest.raises(ValueError, match="Weight must be positive"):
            Pet(id=1, name="Test", species="Dog", age=1, weight=0.0)

        # Test empty name raises error
        with pytest.raises(ValueError, match="Pet name cannot be empty"):
            Pet(id=1, name="", species="Dog", age=1, weight=10.0)


class TestTask:
    """Test cases for the Task class."""

    def test_task_creation_and_completion(self):
        """Test creating a task and marking it complete."""
        # Create a task
        task = Task(
            id=1,
            description="Take Buddy for a walk",
            time="8:00 AM",
            frequency="Daily",
            status=TaskStatus.PENDING
        )

        # Verify task attributes
        assert task.id == 1
        assert task.description == "Take Buddy for a walk"
        assert task.time == "8:00 AM"
        assert task.frequency == "Daily"
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None

        # Complete the task
        result = task.mark_complete()
        assert "completed" in result
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None

        # Verify completion timestamp is recent
        time_diff = datetime.now() - task.completed_at
        assert time_diff.seconds < 10  # Completed within last 10 seconds

    def test_task_validation(self):
        """Test that task validation works correctly."""
        # Test empty description raises error
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            Task(id=1, description="", time="8:00 AM", frequency="Daily")


class TestPetTaskRelationship:
    """Test cases for Pet-Task relationships."""

    def test_adding_task_increases_pet_task_count(self):
        """Test that adding a task to a pet increases the pet's task count."""
        # Create a pet
        pet = Pet(
            id=1,
            name="Max",
            species="Cat",
            age=2,
            weight=12.0,
            health=HealthStatus.EXCELLENT
        )

        # Initially no tasks
        assert len(pet.tasks) == 0
        details = pet.view_details()
        assert details["task_count"] == 0

        # Create and add a task
        task = Task(
            id=1,
            description="Feed Max breakfast",
            time="8:00 AM",
            frequency="Daily"
        )

        pet.add_task(task)

        # Verify task was added and count increased
        assert len(pet.tasks) == 1
        assert pet.tasks[0].description == "Feed Max breakfast"
        assert pet.tasks[0].time == "8:00 AM"

        # Verify through view_details
        details = pet.view_details()
        assert details["task_count"] == 1

    def test_complete_task_changes_status(self):
        """Test that completing a task actually changes its status."""
        # Create a task
        task = Task(
            id=1,
            description="Walk the dog",
            time="8:00 AM",
            frequency="Daily",
            status=TaskStatus.PENDING
        )

        # Verify initial status
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None

        # Complete the task
        result = task.mark_complete()

        # Verify status changed and timestamp was set
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert "completed" in result

        # Verify task details reflect completion
        task_details = task.get_details()
        assert task_details["status"] == "Completed"
        assert task_details["completed_at"] is not None


class TestSchedulerConflictDetection:
    """Test cases for Scheduler conflict detection."""

    def test_detect_same_pet_conflicts(self):
        """Test detection of conflicts where the same pet has multiple tasks at the same time."""
        # Create owner and pets
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet = Pet(id=1, name="TestPet", species="Dog", age=3, weight=25.0)
        owner.add_pet(pet)

        # Create conflicting tasks for the same pet
        task1 = Task(id=1, description="Morning Walk", time="8:00 AM", frequency="Daily")
        task2 = Task(id=2, description="Morning Grooming", time="8:00 AM", frequency="Weekly")
        pet.add_task(task1)
        pet.add_task(task2)

        # Create scheduler and check for conflicts
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts()

        # Should detect the conflict
        assert len(conflicts) == 1
        assert "Time conflict at 8:00 AM" in conflicts[0]
        assert "TestPet: Morning Walk, Morning Grooming" in conflicts[0]

    def test_detect_different_pet_conflicts(self):
        """Test detection of conflicts where different pets have tasks at the same time."""
        # Create owner and pets
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet1 = Pet(id=1, name="Buddy", species="Dog", age=3, weight=25.0)
        pet2 = Pet(id=2, name="Milo", species="Cat", age=2, weight=10.0)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Create tasks at the same time for different pets
        task1 = Task(id=1, description="Training", time="2:00 PM", frequency="Daily")
        task2 = Task(id=2, description="Nap", time="2:00 PM", frequency="Daily")
        pet1.add_task(task1)
        pet2.add_task(task2)

        # Create scheduler and check for conflicts
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts()

        # Should detect the conflict
        assert len(conflicts) == 1
        assert "Multiple pets scheduled at 2:00 PM" in conflicts[0]
        assert "Training, Nap" in conflicts[0]

    def test_no_conflicts_when_tasks_are_at_different_times(self):
        """Test that no conflicts are detected when all tasks are at different times."""
        # Create owner and pet
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet = Pet(id=1, name="TestPet", species="Dog", age=3, weight=25.0)
        owner.add_pet(pet)

        # Create tasks at different times
        task1 = Task(id=1, description="Morning Walk", time="8:00 AM", frequency="Daily")
        task2 = Task(id=2, description="Afternoon Play", time="2:00 PM", frequency="Daily")
        pet.add_task(task1)
        pet.add_task(task2)

        # Create scheduler and check for conflicts
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts()

        # Should not detect any conflicts
        assert len(conflicts) == 0


class TestSchedulerSorting:
    """Test cases for Scheduler sorting functionality."""

    def test_sort_tasks_by_time_chronological_order(self):
        """Test that tasks are sorted correctly by time in chronological order."""
        # Create owner and pet
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet = Pet(id=1, name="TestPet", species="Dog", age=3, weight=25.0)
        owner.add_pet(pet)

        # Create tasks at different times (not in chronological order)
        task1 = Task(id=1, description="Evening Walk", time="6:00 PM", frequency="Daily")
        task2 = Task(id=2, description="Morning Feed", time="8:00 AM", frequency="Daily")
        task3 = Task(id=3, description="Afternoon Play", time="2:00 PM", frequency="Daily")
        task4 = Task(id=4, description="Midnight Check", time="12:00 AM", frequency="Daily")

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        pet.add_task(task4)

        # Create scheduler and sort tasks
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time()

        # Verify tasks are in chronological order
        assert len(sorted_tasks) == 4
        assert sorted_tasks[0].time == "12:00 AM"  # Midnight first
        assert sorted_tasks[1].time == "8:00 AM"   # Morning second
        assert sorted_tasks[2].time == "2:00 PM"   # Afternoon third
        assert sorted_tasks[3].time == "6:00 PM"   # Evening last

        # Verify task descriptions match the expected order
        assert sorted_tasks[0].description == "Midnight Check"
        assert sorted_tasks[1].description == "Morning Feed"
        assert sorted_tasks[2].description == "Afternoon Play"
        assert sorted_tasks[3].description == "Evening Walk"


class TestSchedulerFiltering:
    """Test cases for Scheduler filtering functionality."""

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by completion status."""
        # Create owner and pet
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet = Pet(id=1, name="TestPet", species="Dog", age=3, weight=25.0)
        owner.add_pet(pet)

        # Create tasks with different statuses
        task1 = Task(id=1, description="Pending Task", time="8:00 AM", frequency="Daily", status=TaskStatus.PENDING)
        task2 = Task(id=2, description="Completed Task", time="9:00 AM", frequency="Daily", status=TaskStatus.COMPLETED)
        task3 = Task(id=3, description="Another Pending", time="10:00 AM", frequency="Daily", status=TaskStatus.PENDING)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        # Create scheduler and test filtering
        scheduler = Scheduler(owner)

        # Filter pending tasks
        pending_tasks = scheduler.filter_tasks(status=TaskStatus.PENDING)
        assert len(pending_tasks) == 2
        assert all(task.status == TaskStatus.PENDING for task in pending_tasks)
        assert "Pending Task" in [t.description for t in pending_tasks]
        assert "Another Pending" in [t.description for t in pending_tasks]

        # Filter completed tasks
        completed_tasks = scheduler.filter_tasks(status=TaskStatus.COMPLETED)
        assert len(completed_tasks) == 1
        assert completed_tasks[0].description == "Completed Task"
        assert completed_tasks[0].status == TaskStatus.COMPLETED

    def test_filter_tasks_by_pet_name(self):
        """Test filtering tasks by pet name (case-insensitive)."""
        # Create owner with multiple pets
        owner = Owner(id=1, name="Test Owner", email="test@example.com")
        pet1 = Pet(id=1, name="Buddy", species="Dog", age=3, weight=25.0)
        pet2 = Pet(id=2, name="Milo", species="Cat", age=2, weight=10.0)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Add tasks to each pet
        task1 = Task(id=1, description="Walk Buddy", time="8:00 AM", frequency="Daily")
        task2 = Task(id=2, description="Feed Milo", time="9:00 AM", frequency="Daily")
        task3 = Task(id=3, description="Play with Buddy", time="2:00 PM", frequency="Daily")

        pet1.add_task(task1)
        pet2.add_task(task2)
        pet1.add_task(task3)

        # Create scheduler and test filtering by pet name
        scheduler = Scheduler(owner)

        # Filter tasks for Buddy (case-insensitive)
        buddy_tasks = scheduler.filter_tasks(pet_name="buddy")
        assert len(buddy_tasks) == 2
        assert all("Buddy" in task.description for task in buddy_tasks)

        # Filter tasks for Milo
        milo_tasks = scheduler.filter_tasks(pet_name="MILO")
        assert len(milo_tasks) == 1
        assert milo_tasks[0].description == "Feed Milo"

        # Filter by non-existent pet
        nonexistent_tasks = scheduler.filter_tasks(pet_name="Fluffy")
        assert len(nonexistent_tasks) == 0


class TestTaskRecurrence:
    """Test cases for task recurrence logic."""

    def test_marking_task_complete_does_not_create_new_task(self):
        """Test that marking a task complete does not automatically create a new task.

        Note: Current implementation does not include automatic recurrence.
        This test documents the current behavior and can be updated when
        recurrence logic is implemented.
        """
        # Create a pet and task
        pet = Pet(id=1, name="TestPet", species="Dog", age=3, weight=25.0)
        task = Task(id=1, description="Daily Walk", time="8:00 AM", frequency="Daily")

        pet.add_task(task)

        # Verify initial state
        assert len(pet.tasks) == 1
        assert pet.tasks[0].status == TaskStatus.PENDING

        # Mark task as complete
        task.mark_complete()

        # Verify task is completed but no new task is created
        assert len(pet.tasks) == 1  # Still only one task
        assert pet.tasks[0].status == TaskStatus.COMPLETED
        assert pet.tasks[0].completed_at is not None

        # This test documents current behavior - no automatic recurrence
        # When recurrence is implemented, this test should be updated to expect a new task
