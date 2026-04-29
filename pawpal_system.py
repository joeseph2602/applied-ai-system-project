from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional, List


class HealthStatus(Enum):
    """Enumeration for pet health status levels."""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    CRITICAL = "Critical"


class TaskStatus(Enum):
    """Enumeration for task status."""
    PENDING = "Pending"
    COMPLETED = "Completed"


@dataclass
class Task:
    """Represents a single pet care task."""
    id: int
    description: str
    time: str
    frequency: str
    status: TaskStatus = TaskStatus.PENDING
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if len(self.description.strip()) == 0:
            raise ValueError("Task description cannot be empty")

    def mark_complete(self) -> str:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        return f"Task '{self.description}' marked as completed"

    def get_details(self) -> dict:
        """Return task details."""
        return {
            "id": self.id,
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency,
            "status": self.status.value,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    id: int
    name: str
    species: str
    age: int
    weight: float
    health: HealthStatus = HealthStatus.GOOD
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Validate pet attributes after initialization."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if self.weight <= 0:
            raise ValueError("Weight must be positive")
        if len(self.name.strip()) == 0:
            raise ValueError("Pet name cannot be empty")

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove a task by id."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def view_details(self) -> dict:
        """Return pet details."""
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "weight": self.weight,
            "health": self.health.value,
            "task_count": len(self.tasks)
        }


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    id: int
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by id."""
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    """Organizes and manages tasks across all pets."""
    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """Return only pending tasks."""
        return [task for task in self.get_all_tasks() if task.status == TaskStatus.PENDING]

    def get_completed_tasks(self) -> List[Task]:
        """Return only completed tasks."""
        return [task for task in self.get_all_tasks() if task.status == TaskStatus.COMPLETED]

    def mark_task_complete(self, task_id: int) -> bool:
        """Mark a task complete by id."""
        for task in self.get_all_tasks():
            if task.id == task_id:
                task.mark_complete()
                return True
        return False

    def sort_by_time(self) -> List[Task]:
        """Sort all tasks by their time attribute in ascending order."""
        from datetime import datetime
        
        def time_to_minutes(time_str: str) -> int:
            """Convert time string like '8:00 AM' to minutes since midnight."""
            try:
                # Parse the time string
                time_obj = datetime.strptime(time_str, "%I:%M %p")
                return time_obj.hour * 60 + time_obj.minute
            except ValueError:
                # Fallback: if parsing fails, return a high value to sort to end
                return 9999
        
        return sorted(self.get_all_tasks(), key=lambda task: time_to_minutes(task.time))

    def filter_tasks(self, status: Optional[TaskStatus] = None, pet_name: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by completion status and/or pet name.
        
        Args:
            status: Filter by task status (PENDING, COMPLETED, etc.)
            pet_name: Filter by pet name (case-insensitive)
            
        Returns:
            List of tasks matching the filter criteria
        """
        tasks = self.get_all_tasks()
        
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
            
        if pet_name is not None:
            # Find tasks belonging to pets with the specified name
            filtered_tasks = []
            for task in tasks:
                for pet in self.owner.pets:
                    if task in pet.tasks and pet.name.lower() == pet_name.lower():
                        filtered_tasks.append(task)
                        break
            tasks = filtered_tasks
            
        return tasks

    def detect_conflicts(self) -> List[str]:
        """
        Detect scheduling conflicts where tasks are scheduled at the same time.

        Returns:
            List of warning messages for any conflicts found
        """
        from collections import defaultdict

        warnings = []
        tasks = self.get_all_tasks()

        # Group tasks by time using defaultdict
        time_groups = defaultdict(list)
        for task in tasks:
            time_groups[task.time].append(task)

        # Check for conflicts at each time slot
        for time_slot, conflicting_tasks in time_groups.items():
            if len(conflicting_tasks) > 1:
                # Group tasks by pet using dictionary comprehension
                pet_conflicts = defaultdict(list)
                for task in conflicting_tasks:
                    for pet in self.owner.pets:
                        if task in pet.tasks:
                            pet_conflicts[pet.name].append(task)
                            break

                # Find pets with multiple tasks at this time
                same_pet_conflicts = [
                    f"{pet_name}: {', '.join(t.description for t in pet_tasks)}"
                    for pet_name, pet_tasks in pet_conflicts.items()
                    if len(pet_tasks) > 1
                ]

                if same_pet_conflicts:
                    warnings.append(f"⚠️  Time conflict at {time_slot}: {'; '.join(same_pet_conflicts)}")
                else:
                    # Different pets at same time
                    all_task_descriptions = [t.description for t in conflicting_tasks]
                    warnings.append(f"ℹ️  Multiple pets scheduled at {time_slot}: {', '.join(all_task_descriptions)}")

        return warnings