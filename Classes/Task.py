import re

from Exceptions.DataFormatException import DataFormatException
from Exceptions.TaskFormatException import TaskFormatException


class Task:
    # Nie wolno zmieniac kolejnosci argumentow (finished ma byc ostatni)
    ALLOWED_STATUSES_WITH_ORDER = {
        "ToDo": 0,
        "InProgress": 1,
        "Finished": 2
    }

    ALLOWED_STATUSES = tuple(ALLOWED_STATUSES_WITH_ORDER.keys())
    ALLOWED_PRIORITIES_WITH_ORDER ={
        "UrgentImportant": 3,
        "NotUrgentImportant": 2,
        "UrgentNotImportant": 1,
        "NotUrgentNotImportant": 0
    }
    ALLOWED_PRIORITIES = ALLOWED_PRIORITIES_WITH_ORDER.keys()

    def __init__(self, name, priority, status, due_date, category, description):
        self._name = name
        self._priority = priority
        self._status = status
        self._due_date = due_date
        self._category = category
        self._description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        try:
            if not isinstance(value, str) or value == "":
                raise TaskFormatException("Task name must be a non-empty string.")
            self._name = value
        except TaskFormatException as e:
            raise

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new_priority):
        try:
            if not isinstance(new_priority, str) or new_priority == "":
                raise TaskFormatException("Task priority must be a non-empty string.")

            if new_priority not in Task.ALLOWED_PRIORITIES:
                raise TaskFormatException(
                    """Task priority must be: UrgentImportant, NotUrgentImportant, UrgentNotImportant or NotUrgentNotImportant."""
                )
            self._priority = new_priority
        except TaskFormatException as e:
            raise

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        try:
            if not isinstance(new_status, str) or new_status == "":
                raise TaskFormatException("Task status must be a non-empty string.")
            if new_status not in Task.ALLOWED_STATUSES:
                raise TaskFormatException(
                    """Task status must be: ToDo, InProgress or Finished."""
                )

            self._status = new_status
        except TaskFormatException as e:
            raise

    # @status.setter
    # def status_tweak(self,up_down_change  : bool):
    #     try:
    #         if not isinstance(new_status, str) or new_status == "":
    #             raise TaskFormatException("Task status must be a non-empty string.")
    #         if new_status not in Task.ALLOWED_STATUSES:
    #             raise TaskFormatException(
    #                 """Task status must be: ToDo, InProgress or Finished."""
    #             )
    #
    #         self._status = new_status
    #     except TaskFormatException as e:
    #         raise

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date):
        if (not isinstance(new_due_date, str)
                or new_due_date == ""
                or not re.match(r"^\d{4}-\d{2}-\d{2}$", new_due_date)
        ):

            raise DataFormatException("Task due date must be a non-empty string in a format: YYYY-MM-DD.")
        self._due_date = new_due_date

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        try:
            if not isinstance(new_category, str) or new_category == "":
                raise TaskFormatException("Task category must be a non-empty string.")

            self._category = new_category
        except TaskFormatException as e:
            print(e.message)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        try:
            if not isinstance(new_description, str) or new_description == "":
                raise TaskFormatException("Task description must be a non-empty string.")

            self._description = new_description
        except TaskFormatException as e:
            print(e.message)

    def __str__(self, detailed=False):
        if detailed:
            return (f"Nazwa: {self._name}\n"
                    f"Priorytet: {self._priority}\n"
                    f"Status: {'Do zrobienia 📝' if self._status == Task.ALLOWED_STATUSES[0] else 'W trakcie ⏳' if self._status == Task.ALLOWED_STATUSES[1] else 'Zakończone ✅' if self._status == Task.ALLOWED_STATUSES[2] else self._status}\n"
                    f"Termin: {self._due_date}\n"
                    f"Kategoria: {self._category}\n"
                    f"Opis: {self._description}\n")
        else:
            return (
                f"{self._name}, priority={self._priority}, status={('Do zrobienia 📝' if self._status == Task.ALLOWED_STATUSES[0] else 'W trakcie ⏳' if self._status == Task.ALLOWED_STATUSES[1] else 'Zakończone ✅' if self._status == Task.ALLOWED_STATUSES[2] else self._status)}, due_date={self._due_date}")
