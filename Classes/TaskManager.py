from Classes.Task import Task
from Exceptions.FlagsConflictException import FlagsConflictException
from Exceptions.TaskAlreadyDoneException import TaskAlreadyDoneException
from Exceptions.TaskAlreadyHighestPrioException import TaskAlreadyHighestPrioException
from Exceptions.TaskAlreadyLowestPrioException import TaskAlreadyLowestPrioException
from Exceptions.TaskFormatException import TaskFormatException
import copy
from datetime import date
import matplotlib.pyplot as plt

from Exceptions.UnknownAttributeException import UnknownAttributeException


class TaskManager:
    ALLOWED_DATE_OPTIONS = ("ten_dzien", "ten_tydzien", "ten_miesiac", "ten_rok")

    def __init__(self, task_file_path="Resources/tasksFile.txt"):
        self.tasks = []
        # Sciezka bedzie statyczna do pojedynczego TaskManagera
        self.taskFilePath = task_file_path
        # WARNING: klucze musza odpowiadac nazwą atrybutom z Taska. Nie zmieniaj ich!
        self.filter_dict = {
            'priority': set(),
            'status': set(),
            'due_date': set(),
            'category': set()
        }
        self._allowed_categories = set()
        # Kategoria aktualizują się automatycznie przy dodaniu lub usunięciu zadania za pomocą _update_categories
        self.load_from_file()

    @property
    def allowed_resources(self):
        return {
            'priority': Task.ALLOWED_PRIORITIES,
            'status': Task.ALLOWED_STATUSES,
            'due_date': self.ALLOWED_DATE_OPTIONS,
            'category': self._allowed_categories
        }

    def add_task(self, task: Task) -> None:
        # nazwa musi być unikalna!
        try:
            self._validate_name(task.name)
        except TaskFormatException as e:
            print(f"Nie można dodać zadania: {e.message}")
            return
        self.tasks.append(task)
        self._update_categories()
        print(f"Task '{task}' added.")

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)
            self._update_categories()
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
            self._update_categories()
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
            try:
                task_to_edit.increase_status()
                print(f"Status zadania został podniesiony do {task_to_edit.status}.")
            except TaskAlreadyHighestPrioException as e:
                print(e.message)
            return
        elif '-down' in flags:
            try:
                task_to_edit.decrease_status()
                print(f"Status zadania został obniżony do {task_to_edit.status}.")
            except TaskAlreadyLowestPrioException as e:
                print(e.message)
            return
        elif '-tick' in flags:
            try:
                task_to_edit.mark_as_finished()
                print(f"Zadanie '{task_name}' zostało oznaczone jako ukończone.")
            except TaskAlreadyDoneException as e:
                print(e.message)
            return

        print(f"Edycja zadania: {task_to_edit}")
        while True:
            new_name = input("Podaj nową nazwę: (pozostaw puste, aby zachować obecny)")
            if new_name:
                try:
                    self._validate_name(new_name)
                except TaskFormatException as e:
                    print(f"Nie można dodać zadania: {e.message}")
                    continue
                task_to_edit.name = new_name
                break
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
            # listowanie z uwzględnieniem filtrów
            for task in self.tasks:
                # tutaj metoda _should_be_shown sprawdza, czy zadanie powinno być pokazane na podstawie filtrów
                if self._should_be_shown(task):
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

    def filter_tasks(self, flags : list[str]) -> None:
        while True:
            if '-clear' in flags or '-clr' in flags:
                self.filter_dict = {key: set() for key in self.filter_dict.keys()}
                print("Filtry zostały wyczyszczone.")
                return

            if '-show' in flags:
                if not any(self.filter_dict.values()):
                    print("Brak aktywnych filtrów.")
                else:
                    print("Aktywne filtry:")
                    for key, values in self.filter_dict.items():
                        if values:
                            print(f"\t{key}: {', '.join(values)}")
                return

            filter_attributes = (input(f"Wybierz atrybuty do filtrowania spośród {self.filter_dict.keys()}:")).split(" ")
            if not filter_attributes:
                print("Nie podano atrybutów do filtrowania. Podaj atrybuty ponownie.")
                continue

            for attribute in filter_attributes:
                if attribute not in self.filter_dict:
                    print(f"Atrybut '{attribute}' nie jest prawidłowy. Wybierz spośród {self.filter_dict.keys()}.")
                    continue

            while True:
                print(
                    f"\nPodaj wartości do filtrowania dla atrybutów {', '.join(filter_attributes)}.\n"
                    f"Możliwe wartości dla każdego atrybutu:\n" + "\n".join(
                    f"  {attr}: {', '.join(self.allowed_resources[attr])}" for attr in filter_attributes
                    ))
                filter_values = input("").strip().split(" ")

                for filter_value in filter_values:
                    if filter_value in Task.ALLOWED_PRIORITIES:
                        self.filter_dict['priority'].add(filter_value)
                    elif filter_value in Task.ALLOWED_STATUSES:
                        self.filter_dict['status'].add(filter_value)
                    elif filter_value in self.ALLOWED_DATE_OPTIONS:
                        self.filter_dict['due_date'].add(filter_value)
                    elif filter_value in self._allowed_categories:
                        self.filter_dict['category'].add(filter_value)
                    else:
                        print(f"Wartość '{filter_value}' nie jest prawidłowa dla żadnego atrybutu.")
                        continue

                print(
                    f"Zadania będą filtrowane według: {', '.join(f'{key}: {values}' for key, values in self.filter_dict.items() if values)}")
                break
            return

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

    def display_statistics(self) -> None:
        status_occurrences = {status: 0 for status in Task.ALLOWED_STATUSES}
        for task in self.tasks:
            status_occurrences[task.status] += 1
        kolory = ['#ffb3ba', '#baffc9', '#bae1ff']  # pastelowe kolory
        plt.pie(status_occurrences.values(), labels=status_occurrences.keys(), autopct='%1.1f%%', colors=kolory,
                startangle=90)
        plt.title("Statystyki zadań według statusu")
        plt.show()

        category_occurrences = {category: 0 for category in self._allowed_categories}

        for task in self.tasks:
            category_occurrences[task.category] += 1
        plt.pie(category_occurrences.values(), labels=category_occurrences.keys(), autopct='%1.1f%%',
                startangle=90)
        plt.title("Statystyki zadań według kategorii")
        plt.show()

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
                self._update_categories()
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

    def _validate_name(self, name: str) -> None:
        if any(task.name == name for task in self.tasks):
            raise TaskFormatException(f"Task with name '{name}' already exists.")

    def _update_categories(self) -> None:
        self._allowed_categories = set(task.category for task in self.tasks if task.category)

    def _should_be_shown(self, task: Task) -> bool:
        for key_attr, values in self.filter_dict.items():
            # tutaj jest sprytnie jak wartości dicta są puste to pokazujemy wszystkie, jak nie, to sprawdzamy te, które są czy takie same jak w obiekcie do wyświetlenia
            if values:
                if key_attr == 'due_date':
                    today = date.today()
                    task_date = tuple(map(int, task.due_date.split('-')))
                    today_date = (today.year, today.month, today.day)
                    if 'ten_dzien' in values and task_date != today_date:
                        return False
                    if 'ten_tydzien' in values:
                        task_dt = date(task_date[0], task_date[1], task_date[2])
                        if task_dt.isocalendar()[:2] != today.isocalendar()[:2]:
                            return False
                    if 'ten_miesiac' in values and not (task_date[0] == today.year and task_date[1] == today.month):
                        return False
                    if 'ten_rok' in values and task_date[0] != today.year:
                        return False
                    continue
                if getattr(task, key_attr) not in values:
                    return False
        return True
