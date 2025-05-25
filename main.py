import pyreadline3
#implementacja pod cmd zeby pamietac komendy, ale nie wiem, czy to chcemy

from Classes.Task import Task
from Classes.TaskManager import TaskManager
from datetime import date

taskManager = TaskManager()
today = date.today()
isRunning = True
print("============================================================================")
print("====================== 🌟 Witaj w Task Managerze 🌟 =======================")
print("============================================================================")
print("📅 Mamy dzisiaj: " + today.strftime("%Y-%m-%d"))
print("🤖 Pomogę Ci zarządzać Twoimi zadaniami! 💼")
print()
print(" help              Wyświetl dostępne polecenia")
try:
    while isRunning:
        # INFO: tutaj strip() i [0] zeby tylko komenda była zmniejszana, a nie reszta
        command = input("Wpisz polecenie >").strip()
        # INFO: tutaj zeby nie było problemu z wielkością liter
        command_parts = command.split(" ")
        choice = command_parts[0].lower()
        command_parts.remove(choice)
        flags = [i for i in command_parts if i.startswith('-') or i.startswith('--')]
        # command_suffix = [i for i in command_parts if not (i.startswith('-') or i.startswith('--'))]
        command_suffix = [i for i in command_parts if i not in flags]


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
            if not command_suffix:
                name = input("Podaj nazwę zadania do edycji: ")
            else:
                name = command_suffix[0]
            taskManager.edit_task_by_name(flags ,name)
        elif choice == 'list' or choice == 'ls':
            taskManager.list_tasks(flags)
        elif choice == 'show':
            if not command_suffix:
                name = input("Podaj nazwę zadania do wyświetlenia: ")
            else:
                name = command_suffix[0]
            taskManager.show_task_details(name)
        elif choice == 'filter':
            #TODO: implement
            taskManager.filter_tasks(flags)
        elif choice == 'sort':
            taskManager.sort_tasks(flags,*command_suffix)
        elif choice == 'display':
            #TODO: implement
            taskManager.display_statistics()
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
            print(" list [-less]                   Wyświetl wszystkie zadania spełniające filtr (lub 'ls') (flaga -less wyświetli z opisami)")
            print(" show <name>                    Wyświetl szczegóły zadania o podanej nazwie")
            print(" filter [-clear/-show]          Wybierz w jaki sposób chcesz filtrować zadania (np. po statusie, priorytecie, kategorii itp.)\n"
                  "                                (flaga -clear lub -clr czyści wszystkie filtry oraz -show wyświetla aktualne filtry)")
            print(" sort <attributes> [-r]         Sortuj rosnąco zadania po atrybucie (np. 'priority', 'status', 'due_date') (flaga -r odwróci sortowanie)")
            print(" display                        Wyświetl statystyki zadań za pomocą wykresów")
            print(" commit                         Zapisz aktualny stan zadań do pliku (Uwaga: nadpisuje plik i jest nieodwracalne)")
            print(" rollback                       Wczytaj ostatni stan zadań z pliku")
            print(" exit                           Zakończ program")
except KeyboardInterrupt:
    print("\n\nPrzerwano program. Transakcja została anulowana.")