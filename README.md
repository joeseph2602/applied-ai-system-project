# PawPal AI System

## Original Project
This project is based on a pet care management system from previous modules. The original goal was to help pet owners organize and track pet care tasks, such as feeding, walking, and vet visits.

## Title and Summary
**PawPal** is an AI-assisted pet care scheduler. It helps pet owners manage daily and special tasks for their pets, detects scheduling conflicts, and logs all actions for reliability and review.

## Architecture Overview
- Main components: Owner, Pet, Task, Scheduler, Logger, and a Reliability Tester.
- Data flows from user input (pet/task info) to the Scheduler, which manages and checks tasks, logs actions, and outputs results for user review.
- See `assets/system_diagram.md` for a visual diagram.

## Setup Instructions
1. Clone/download the project.
2. Ensure you have Python 3.8+ installed.
3. Run `python main.py` to see the demo.
4. Run `python reliability_test.py` to check system reliability and view logs in `pawpal.log`.

## Sample Interactions
- Adding a pet and tasks:
  - Input: Add pet "Buddy" and task "Morning Walk" at 8:00 AM.
  - Output: Task is scheduled for Buddy at 8:00 AM.
- Detecting conflicts:
  - Input: Add two tasks for the same pet at the same time.
  - Output: System warns of a scheduling conflict.
- Marking a task complete:
  - Input: Mark "Morning Walk" as complete.
  - Output: Task status changes to completed and is logged.

## Design Decisions
- Used Python dataclasses for simple, readable code.
- Added a logger for traceability and reliability.
- Chose a reliability test script for easy, repeatable testing.

## Testing Summary
- The system correctly detects conflicts, marks tasks complete, and logs actions.
- Reliability tests run automatically and results are visible in the log file.
- All features work as expected in a simple environment.

## Reflection
This project taught me how to integrate reliability and logging into an AI-assisted workflow, and the importance of clear data flow and testing for robust systems.
