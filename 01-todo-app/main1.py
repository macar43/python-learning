import sys

# Function to display the menu
def display_menu():
    print("\nTo-Do List CLI Application")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Remove task")
    print("5. Exit")

# Function to add a task
def add_task(tasks):
    task = input("Enter the task: ")
    tasks.append({'task': task, 'completed': False})
    print(f'Task added: {task}')

# Function to view tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
    else:
        print("\nTasks:")
        for index, task in enumerate(tasks):
            status = "[x]" if task['completed'] else "[ ]"
            print(f'{index + 1}. {status} {task['task']}')

# Function to mark a task as completed
def complete_task(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter the task number to complete: "))
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]['completed'] = True
            print(f'Task completed: {tasks[task_number - 1]['task']}')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to remove a task
def remove_task(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter the task number to remove: "))
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            print(f'Task removed: {removed_task['task']}')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Main function to run the application
def main():
    tasks = []
    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            remove_task(tasks)
        elif choice == '5':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()