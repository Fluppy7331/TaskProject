from Classes.Task import Task
from Exceptions.FlagsConflictException import FlagsConflictException
from Exceptions.TaskFormatException import TaskFormatException
import copy


class TaskManager:
    def __init__(self, task_file_path="Resources/tasksFile.txt"):
        self.tasks = []
        # Sciezka bedzie statyczna do pojedynczego TaskManagera
        self.taskFilePath = task_file_path
        self.load_from_file()

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        print(f"Task '{task}' added.")

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Task '{task}' removed.")
        else:
            print(f"Task '{task}' not found.")

    def remove_task_by_name(self, task_name: str) -> None:
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

    def edit_task_by_name(self, flags: list[str], task_name: str) -> None:
        task_to_edit = None
        task_before_edit = None
        for task in self.tasks:
            if task.name == task_name:
                task_to_edit = task
                task_before_edit = copy.deepcopy(task)
                break
        if not task_to_edit:
            print(f"Task '{task_name}' not found.")
            return

        if len(flags) > 1:
            raise FlagsConflictException("Provided flags are conflicting. Please use only one flag at a time.")
        # TODO: mozna jakos to lepiej zrobic, ale na razie nie ma potrzeby

        if '-up' in flags:
            current_status = task_to_edit.status
            current_status_index = Task.ALLOWED_STATUSES.index(current_status)
            if current_status_index < len(Task.ALLOWED_STATUSES) - 1:
                task_to_edit.status = Task.ALLOWED_STATUSES[current_status_index + 1]
                print(f"Status zadania został podniesiony do {task_to_edit.status}.")
            else:
                print("Status zadania jest już na najwyższym poziomie.")
        elif '-down' in flags:
            current_status = task_to_edit.status
            current_status_index = Task.ALLOWED_STATUSES.index(current_status)
            if current_status_index > 0:
                task_to_edit.status = Task.ALLOWED_STATUSES[current_status_index - 1]
                print(f"Status zadania został obniżony do {task_to_edit.status}.")
            else:
                print("Status zadania jest już na najniższym poziomie.")
        elif '-tick' in flags:
            if task_to_edit.status == Task.ALLOWED_STATUSES[-1]:  # Finished
                print("Zadanie jest już ukończone.")
                return
            else:
                task_to_edit.status = Task.ALLOWED_STATUSES[-1]
                print(f"Zadanie '{task_name}' zostało oznaczone jako ukończone.")
                return
        #Todo : trzeba zrobic obsluge w klasie i rzucic bledem jak jest max bedzie ladniej skladniowo
        print(f"Edycja zadania: {task_to_edit}")
        new_name = input("Podaj nową nazwę: (pozostaw puste, aby zachować obecny)")
        if new_name:
            task_to_edit.name = new_name
        while True:
            try:
                new_priority = input(
                    f"Podaj nowy priorytet (pozostaw puste, aby zachować obecny)\n(dostępne: {', '.join(Task.ALLOWED_PRIORITIES)}): ")
                if new_priority:
                    task_to_edit.priority = new_priority
                break
            except TaskFormatException as e:
                print(f"Nieprawidłowy priorytet: {e.message}")
                continue

        while True:
            try:
                new_status = input(
                    f"Podaj nowy status (pozostaw puste, aby zachować obecny)\n(dostępne: {', '.join(Task.ALLOWED_STATUSES)}): ")
                if new_status:
                    task_to_edit.status = new_status
                break
            except TaskFormatException as e:
                print(f"Nieprawidłowy status: {e.message}")
                continue

        while True:
            try:
                new_due_date = input("Podaj nowy termin (pozostaw puste, aby zachować obecny) (format:YYYY-MM-DD): ")
                if new_due_date:
                    task_to_edit.due_date = new_due_date
                break
            except TaskFormatException as e:
                print(f"Nieprawidłowy termin: {e.message}")
                continue

        new_category = input("Podaj nową kategorię (pozostaw puste, aby zachować obecną): ")
        if new_category:
            task_to_edit.category = new_category

        new_description = input("Podaj nowy opis (pozostaw puste, aby zachować obecny): ")
        if new_description:
            task_to_edit.description = new_description

        final_decision = input(f"Czy chcesz zapisać zmiany w zadaniu '{task_name}'? (t/n): ").strip().lower()
        if final_decision != 't':
            # Przywracanie stanu przed edycją
            if task_before_edit:
                task_to_edit.name = task_before_edit.name
                task_to_edit.priority = task_before_edit.priority
                task_to_edit.status = task_before_edit.status
                task_to_edit.due_date = task_before_edit.due_date
                task_to_edit.category = task_before_edit.category
                task_to_edit.description = task_before_edit.description
                print(f"Zmiany w zadaniu '{task_name}' zostały anulowane.")
            return
        print(f"Task '{task_name}' updated. (Remember to use 'commit' to save changes.)")

    def list_tasks(self, flags: list[str]) -> None:
        detailed = False
        if '-less' in flags: detailed = True
        if not self.tasks:
            print("No tasks available.")
        else:
            print("Tasks:")
            for task in self.tasks:
                print(f"- {task.__str__(detailed=detailed)}")

    def show_task_details(self, task_name: str) -> None:
        task_to_show = None
        for task in self.tasks:
            if task.name == task_name:
                task_to_show = task
                break
        if not task_to_show:
            print(f"Task '{task_name}' not found.")
            return
        print(f"Details for task '{task_name}':\n{task_to_show.__str__(detailed=True)}")

    def sort_tasks(self, flags: list[str], *args: str) -> None:
        reverse = False
        if not args:
            print("Podaj atrybuty do sortowania, np. sort_tasks('priority', 'status', 'due_date')")
            return
        try:
            if '-r' in flags:
                reverse = True
                args = list(args)
                args.remove('-r')

            # Unikalne atrybuty do sortowania rozwiazane we wlasnym kluczu
            def my_key(task):
                key = []
                for attr in args:
                    value = getattr(task, attr)
                    if attr == "priority":
                        value = Task.ALLOWED_PRIORITIES_WITH_ORDER.get(value, 99)
                    elif attr == "status":
                        value = Task.ALLOWED_STATUSES_WITH_ORDER.get(value, 99)
                    key.append(value)
                return tuple(key)

            self.tasks.sort(key=my_key, reverse=reverse)
            print(f"Zadania posortowane według: {', '.join(args)}. Kolejność: {'malejąco' if reverse else 'rosnąco'}.")
        except AttributeError as e:
            print(f"Błąd sortowania: {e}")

    def load_from_file(self) -> None:
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

    def save_to_file(self) -> None:
        try:
            with open(self.taskFilePath, 'w', encoding='utf-8') as file:
                for task in self.tasks:
                    file.write(','.join([task.name, task.priority, task.status, task.due_date, task.category,
                                         task.description]) + '\n')
            print(f"Tasks saved to '{self.taskFilePath}'.")
        except Exception as e:
            print(f"Error saving tasks: {e}")
