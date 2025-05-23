from Classes.Task import Task
from Exceptions.TaskFormatException import TaskFormatException


class TaskManager:
    def __init__(self, taskFilePath="Resources/tasksFile.txt"):
        self.tasks = []
        # Sciezka bedzie statyczna do pojedynczego TaskManagera
        self.taskFilePath = taskFilePath
        self.load_from_file()

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task}' added.")

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Task '{task}' removed.")
        else:
            print(f"Task '{task}' not found.")

    def remove_task_by_name(self, task_name: str):
        task_to_remove = None
        for task in self.tasks:
            if task.name == task_name:
                task_to_remove = task
                break
        if task_to_remove:
            self.tasks.remove(task_to_remove)
            print(f"Task '{task_name}' removed.")
        else:
            print(f"Task '{task_name}' not found.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            print("Tasks:")
            for task in self.tasks:
                print(f"- {task}")

    def sort_tasks(self, *args):
        reverse = False
        if not args:
            print("Podaj atrybuty do sortowania, np. sort_tasks('priority', 'status', 'due_date')")
            return
        try:
            if '-r' in args:
                reverse = True
                args = list(args)
                args.remove('-r')
            self.tasks.sort(key=lambda task: tuple(getattr(task, attr) for attr in args),reverse=reverse)
            # TODO : unikalne sortowanie dla priorytetów itd
            print(f"Zadania posortowane według: {', '.join(args)}. Kolejność: {'malejąco' if reverse else 'rosnąco'}.")
        except AttributeError as e:
            print(f"Błąd sortowania: {e}")

    def load_from_file(self):
        try:
            with open(self.taskFilePath, 'r', encoding='utf-8') as file:
                temp_tasks = []
                for line in file:
                    # Tutaj taki feature zeby wygodnie pomijac komentarze i puste linie
                    if line.startswith('#') or not line.strip():
                        continue
                    task_data = line.strip().split(',')
                    if len(task_data) != 6:
                        raise TaskFormatException("Task data must contain exactly 6 fields.")
                    task = Task(*task_data)
                    temp_tasks.append(task)
                self.tasks = temp_tasks
        except FileNotFoundError:
            print(f"File '{self.taskFilePath}' not found.")
        except TaskFormatException as e:
            print(e.message)

    def save_to_file(self):
        try:
            with open(self.taskFilePath, 'w', encoding='utf-8') as file:
                for task in self.tasks:
                    file.write(','.join([task._name, task._priority, task._status, task._due_date, task._category,
                                         task._description]) + '\n')
            print(f"Tasks saved to '{self.taskFilePath}'.")
        except Exception as e:
            print(f"Error saving tasks: {e}")
