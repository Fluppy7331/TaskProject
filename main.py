from Classes.Task import Task
from Classes.TaskManager import TaskManager

taskManager = TaskManager()
isRunning = True
print("========================== Witaj w Task Managerze ==========================")
print()
print(" help              Wyświetl dostępne polecenia")

while isRunning:

    # INFO: tutaj strip() i [0] zeby tylko komenda była zmniejszana a nie reszta
    command = input("Wpisz polecenie >").strip()
    # INFO: tutaj zeby nie było problemu z wielkością liter
    command_parts = command.split(" ")
    choice = command_parts[0].lower()
    command_suffix = command_parts[1:] if len(command_parts)>1 else None


    if choice == 'add':
        name = input("Podaj nazwę zadania: ")
        priority = input("Podaj priorytet zadania: ")
        status = input("Podaj status zadania: ")
        due_date = input("Podaj termin wykonania zadania: ")
        category = input("Podaj kategorię zadania: ")
        description = input("Podaj opis zadania: ")
        #tworzenie obiektu Task zeby przeszedł wstępne walidacje
        taskManager.add_task(Task(name, priority, status, due_date, category, description))
    elif choice == 'remove' and command_suffix is None:
        name = input("Podaj nazwę zadania do usunięcia: ")
        taskManager.remove_task_by_name(name)
    elif choice == 'remove' and command_suffix is not None:
        taskManager.remove_task_by_name(command_suffix[0])
    elif choice == 'list' or choice == 'ls':
        taskManager.list_tasks()
    elif choice == 'sort':
        taskManager.sort_tasks(*command_suffix)
    elif choice == 'commit':
        taskManager.save_to_file()
    elif choice == 'rollback':
        print("Zadania zostały przywrócone z pliku...")
        taskManager.load_from_file()
    elif choice == 'exit':
        isRunning = False
    else:
        if choice!= "help":print(f"Nieprawidłowe polecenie: '{choice}' Spróbuj ponownie.")
        print("Dostępne polecenia:")

        print(" add                     Dodaj nowe zadanie")
        print(" remove <name>           Usuń istniejące zadanie")
        print(" list                    Wyświetl wszystkie zadania")
        print(" sort <attributes> [-r]  Sortuj rosnąco zadania po atrybucie (np. 'priority', 'status', 'due_date') (flaga -r odwróci sortowanie)")
        print(" commit                  Zapisz aktualny stan zadań do pliku (Uwaga: nadpisuje plik i jest nieodwracalne)")
        print(" rollback                Wczytaj ostatni stan zadań z pliku")
        print(" exit                    Zakończ program")
