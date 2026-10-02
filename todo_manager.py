import json
import os
from datetime import datetime


FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tasks.json"
)


def load_tasks():
    """Load tasks from JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                return []

            # Add default values for older tasks
            for task in data:
                task.setdefault("priority", "Medium")
                task.setdefault("due_date", "")
                task.setdefault("tags", [])

            return data

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load tasks.")
        return []


def save_tasks(tasks):
    """Save tasks to JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

        print("Tasks saved successfully.")

    except OSError:
        print("Error: Could not save tasks.")


def get_priority():
    """Get valid priority from user."""
    while True:
        print("\nPriority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")

        choice = input("Choose priority: ").strip()

        priorities = {
            "1": "High",
            "2": "Medium",
            "3": "Low"
        }

        if choice in priorities:
            return priorities[choice]

        print("Invalid priority. Please choose 1-3.")


def get_due_date():
    """Get optional valid due date."""
    while True:
        due_date = input(
            "Enter due date (DD-MM-YYYY) or press Enter to skip: "
        ).strip()

        if not due_date:
            return ""

        try:
            datetime.strptime(due_date, "%d-%m-%Y")
            return due_date

        except ValueError:
            print("Invalid date format. Use DD-MM-YYYY.")


def get_tags():
    """Get comma-separated tags."""
    tags_input = input(
        "Enter tags separated by commas (optional): "
    ).strip()

    if not tags_input:
        return []

    return [
        tag.strip()
        for tag in tags_input.split(",")
        if tag.strip()
    ]


def add_task(tasks):
    """Add a new task."""
    title = input("\nEnter task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    priority = get_priority()
    due_date = get_due_date()
    tags = get_tags()

    task = {
        "title": title,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "tags": tags
    }

    tasks.append(task)
    save_tasks(tasks)

    print("\nTask added successfully.")


def display_task(index, task):
    """Display one task."""
    status = "Done" if task.get("completed", False) else "Pending"

    priority = task.get("priority", "Medium")
    due_date = task.get("due_date", "")
    tags = task.get("tags", [])

    print(f"\n{index}. {task['title']}")
    print(f"   Status   : {status}")
    print(f"   Priority : {priority}")
    print(f"   Due Date : {due_date if due_date else 'Not set'}")
    print(
        f"   Tags     : {', '.join(tags) if tags else 'No tags'}"
    )


def view_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n========== YOUR TASKS ==========")

    for index, task in enumerate(tasks, start=1):
        display_task(index, task)

    print("\n================================")


def mark_task_done(tasks):
    """Mark a task as completed."""
    if not tasks:
        print("\nNo tasks available.")
        return

    view_tasks(tasks)

    try:
        number = int(input("\nEnter task number to mark as done: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number.")
            return

        if tasks[number - 1]["completed"]:
            print("Task is already completed.")
            return

        tasks[number - 1]["completed"] = True
        save_tasks(tasks)

        print("Task marked as completed.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task(tasks):
    """Delete a task."""
    if not tasks:
        print("\nNo tasks available.")
        return

    view_tasks(tasks)

    try:
        number = int(input("\nEnter task number to delete: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number.")
            return

        deleted_task = tasks.pop(number - 1)

        save_tasks(tasks)

        print(f"Task deleted: {deleted_task['title']}")

    except ValueError:
        print("Please enter a valid number.")


def edit_task(tasks):
    """Edit an existing task."""
    if not tasks:
        print("\nNo tasks available.")
        return

    view_tasks(tasks)

    try:
        number = int(input("\nEnter task number to edit: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[number - 1]

        print("\nLeave input empty to keep the existing value.")

        new_title = input(
            f"Task [{task['title']}]: "
        ).strip()

        if new_title:
            task["title"] = new_title

        print(f"\nCurrent priority: {task.get('priority', 'Medium')}")
        change_priority = input(
            "Change priority? (y/n): "
        ).strip().lower()

        if change_priority == "y":
            task["priority"] = get_priority()

        print(
            f"\nCurrent due date: "
            f"{task.get('due_date') or 'Not set'}"
        )

        change_date = input(
            "Change due date? (y/n): "
        ).strip().lower()

        if change_date == "y":
            task["due_date"] = get_due_date()

        print(
            f"\nCurrent tags: "
            f"{', '.join(task.get('tags', [])) or 'No tags'}"
        )

        change_tags = input(
            "Change tags? (y/n): "
        ).strip().lower()

        if change_tags == "y":
            task["tags"] = get_tags()

        save_tasks(tasks)

        print("Task updated successfully.")

    except ValueError:
        print("Please enter a valid number.")


def search_tasks(tasks):
    """Search tasks by title or tag."""
    if not tasks:
        print("\nNo tasks available.")
        return

    keyword = input(
        "\nEnter keyword to search: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    found = False

    print("\n========== SEARCH RESULTS ==========")

    for index, task in enumerate(tasks, start=1):
        title = task["title"].lower()

        tags = [
            tag.lower()
            for tag in task.get("tags", [])
        ]

        if keyword in title or any(keyword in tag for tag in tags):
            display_task(index, task)
            found = True

    if not found:
        print("No matching tasks found.")

    print("====================================")


def task_summary(tasks):
    """Display task statistics."""
    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task.get("completed", False)
    )

    pending = total - completed

    high_priority = sum(
        1 for task in tasks
        if task.get("priority") == "High"
        and not task.get("completed", False)
    )

    print("\n========== TASK SUMMARY ==========")
    print(f"Total Tasks       : {total}")
    print(f"Completed Tasks   : {completed}")
    print(f"Pending Tasks     : {pending}")
    print(f"High Priority     : {high_priority}")
    print("==================================")


def clear_completed(tasks):
    """Delete all completed tasks."""
    completed_count = sum(
        1 for task in tasks
        if task.get("completed", False)
    )

    if completed_count == 0:
        print("\nNo completed tasks found.")
        return

    confirmation = input(
        f"Delete {completed_count} completed task(s)? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        tasks[:] = [
            task for task in tasks
            if not task.get("completed", False)
        ]

        save_tasks(tasks)

        print("Completed tasks cleared.")

    else:
        print("Operation cancelled.")


def main():
    """Main menu."""
    tasks = load_tasks()

    while True:

        print("\n")
        print("========== ADVANCED TO-DO LIST ==========")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Search Task")
        print("7. Task Summary")
        print("8. Clear Completed Tasks")
        print("9. Exit")
        print("==========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            mark_task_done(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            edit_task(tasks)

        elif choice == "6":
            search_tasks(tasks)

        elif choice == "7":
            task_summary(tasks)

        elif choice == "8":
            clear_completed(tasks)

        elif choice == "9":
            print("\nThank you for using Advanced To-Do List Manager!")
            break

        else:
            print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()