import sys
import json
import os
file_path = 'list.json'
class Task:
    next_id = 1
    def __init__(self, description, status="in progress", task_id=None):
        if task_id is None:
            self.id = Task.next_id
            Task.next_id += 1
        else:
            self.id = task_id
            if task_id >= Task.next_id:
                Task.next_id = task_id + 1
        self.description = description
        self.status = status

    def update_status(self, new_status):
        self.status = new_status.lower()

    def to_dict(self):
        return {"id": self.id, "description": self.description, "status": self.status}

    @staticmethod
    def from_dict(data):
        return Task(description=data["description"], status=data["status"], task_id=data["id"])

def load_tasks():
    tasks = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                tasks = [Task.from_dict(item) for item in data]
            except json.JSONDecodeError:
                tasks = []
        return tasks

def save_tasks(tasks):    
    with open(file_path, 'w') as f:
        json.dump([task.to_dict() for task in tasks] ,f, indent=2)

def add_task(tasks, description):
    task = Task(description)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task.id}, {task.description}, {task.status}")

def update_task(tasks, task_id, new_status):
    for task in tasks:
        if task.id == task_id:
            task.update_status(new_status)
            save_tasks(tasks)
            print(f"Task updated: {task.id} {task.status}")
            return
    print(f"No task found with ID {task_id}")

def delete_task(tasks, task_id):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            removed_task = tasks.pop(i)
            save_tasks(tasks)
            print(f"Task deleted: ID {removed_task.id}, {removed_task.description}")
            return
    print(f"No task found with ID {task_id}")

def list_task(tasks):
    for task in tasks:
        print(f"{task.id}, {task.description}")
            

def list_status(tasks, status_filter=None):
    filtered_status = tasks
    if status_filter:
        filtered_tasks = [task for task in tasks if task.status.lower() == status_filter.lower()]
    if not filtered_status:
        print("No task found")
        return
    for task in filtered_tasks:
        print(f"{task.id}, {task.description}, {task.status}")

    
    

def main():
    tasks = load_tasks()

    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [arguments]")
        return
    command = sys.argv[1].lower()
            
    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: please provide a task description")
        else:
            description = " ".join(sys.argv[2:])
            add_task(tasks, description)
        
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Error: please provide task id and new status")
        else:
            try:
                task_id = int(sys.argv[2])
                new_status = sys.argv[3]
                update_task(tasks, task_id, new_status)
            except ValueError:
                print("Error: Task ID must be a number")
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: please provide task ID to delete")
        else:
            try:
                task_id = int(sys.argv[2])
                delete_task(tasks, task_id)
            except ValueError:
                print("Error: Task ID must be a number")
    
    elif command == 'list':
        list_task(tasks)
    elif command == 'status':
        if len(sys.argv) >= 3:
            status_filter = " ".join(sys.argv[2:])
            list_status(tasks, status_filter)
        else:
            list_status(tasks)


    
    
    

if __name__ == "__main__":
    main()


    

        