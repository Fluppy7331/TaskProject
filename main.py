import pyreadline3
#implementacja pod cmd zeby pamietac komendy, ale nie wiem, czy to chcemy

from Classes.Task import Task
from Classes.TaskManager import TaskManager

taskManager = TaskManager()
isRunning = True
print("========================== Witaj w Task Managerze ==========================")
print()
print(" help              Wyświetl dostępne polecenia")

while isRunning:

    # INFO: tutaj strip() i [0] zeby tylko komenda była zmniejszana, a nie reszta
    command = input("Wpisz polecenie >").strip()
    # INFO: tutaj zeby nie było problemu z wielkością liter
    command_parts = command.split(" ")
    choice = command_parts[0].lower()
    command_parts.remove(choice)
    flags = [i for i in command_parts if i.startswith('-') or i.startswith('--')]
    command_suffix = [i for i in command_parts if not (i.startswith('-') or i.startswith('--'))]


    if choice == 'add':
        name = input("Podaj nazwę zadania: ")
        priority = input("Podaj priorytet zadania: ")
        status = input("Podaj status zadania: ")
        due_date = input("Podaj termin wykonania zadania: ")
        category = input("Podaj kategorię zadania: ")
        description = input("Podaj opis zadania: ")
        #tworzenie obiektu Task, żeby przeszedł wstępne walidacje
        taskManager.add_task(Task(name, priority, status, due_date, category, description))
    elif choice == 'remove' and command_suffix is None:
        name = input("Podaj nazwę zadania do usunięcia: ")
        taskManager.remove_task_by_name(name)
    elif choice == 'remove' and command_suffix is not None:
        taskManager.remove_task_by_name(command_suffix[0])
    elif choice == 'edit':
        if command_suffix is None:
            name = input("Podaj nazwę zadania do edycji: ")
        else:
            name = command_suffix[0]
        taskManager.edit_task_by_name(flags ,name)
    elif choice == 'list' or choice == 'ls':
        taskManager.list_tasks(flags)
    elif choice == 'show':
        if command_suffix is None:
            name = input("Podaj nazwę zadania do wyświetlenia: ")
        else:
            name = command_suffix[0]
        taskManager.show_task_details(name)
    elif choice == 'sort':
        taskManager.sort_tasks(flags,*command_suffix)
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

        print(" add                            Dodaj nowe zadanie")
        print(" remove <name>                  Usuń istniejące zadanie")
        print(" edit <name> [-up/-down/-tick]  Edytuj istniejące zadanie (przejdź do edycji, a następnie użyj 'commit' aby zapisać zmiany)\n"
              "                                (flagi -up/-down/-tick ,które zmieniają status status wyżej/niżej/zakończone gdzie najniższy to 'ToDo')")
        print(" list [-less]                   Wyświetl wszystkie zadania (lub 'ls') (flaga -less wyświetli z opisami)")
        print(" show <name>                    Wyświetl szczegóły zadania o podanej nazwie")
        print(" sort <attributes> [-r]         Sortuj rosnąco zadania po atrybucie (np. 'priority', 'status', 'due_date') (flaga -r odwróci sortowanie)")
        print(" commit                         Zapisz aktualny stan zadań do pliku (Uwaga: nadpisuje plik i jest nieodwracalne)")
        print(" rollback                       Wczytaj ostatni stan zadań z pliku")
        print(" exit                           Zakończ program")
