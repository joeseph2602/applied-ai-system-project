from pawpal_system import Owner, Pet, Task, Scheduler, TaskStatus
from logger import log_action, log_error

def run_reliability_tests():
    try:
        owner = Owner(id=99, name="TestOwner", email="test@example.com")
        pet = Pet(id=1, name="TestPet", species="Dog", age=5, weight=20.0)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Add tasks
        t1 = Task(id=1, description="Test Task 1", time="8:00 AM", frequency="Daily")
        t2 = Task(id=2, description="Test Task 2", time="8:00 AM", frequency="Daily")  # Intentional conflict
        pet.add_task(t1)
        pet.add_task(t2)
        log_action("Added test tasks for reliability test.")

        # Test: Mark task complete
        scheduler.mark_task_complete(t1.id)
        assert t1.status == TaskStatus.COMPLETED, "Task completion failed!"
        log_action("Task completion test passed.")

        # Test: Conflict detection
        conflicts = scheduler.detect_conflicts()
        assert conflicts, "Conflict detection failed!"
        log_action(f"Conflict detection test passed. Conflicts: {conflicts}")

        # Test: Logging works (check pawpal.log manually)
        print("Reliability tests completed. Check pawpal.log for details.")
    except Exception as e:
        log_error(f"Reliability test error: {e}")
        print(f"Reliability test failed: {e}")

if __name__ == "__main__":
    run_reliability_tests()
