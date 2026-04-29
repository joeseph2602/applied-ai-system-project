# PawPal System Architecture

```mermaid
flowchart TD
    A[User Input (Owner/Pet/Task Data)] --> B[Scheduler]
    B --> C[Task Management]
    C --> D[Conflict Detection]
    C --> E[Task Completion]
    D --> F[Logger]
    E --> F
    F --> G[Log File (pawpal.log)]
    C --> H[Output: Task List, Status, Conflicts]
    H --> I[User Review]
    subgraph Testing
        J[reliability_test.py]
        J --> F
        J --> H
    end
    I -. Human checks results .-> H
    J -. Automated checks .-> H
```

## Diagram Explanation
- **Main Components:** Scheduler, Task Management, Conflict Detection, Task Completion, Logger, Log File, Output, User Review, reliability_test.py
- **Data Flow:** User input → Scheduler → Task Management → (Task Completion/Conflict Detection) → Logger → Log File → Output → User Review
- **Testing:** Both humans and the reliability_test.py script check results and system reliability.
