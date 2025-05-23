import re

from Exceptions.DataFormatException import DataFormatException
from Exceptions.TaskFormatException import TaskFormatException


class Task:
    # Nie wolno zmieniac kolejnosci argumentow
    ALLOWED_STATUSES_WITH_ORDER = ("ToDo", "InProgress", "Finished")
    ALLOWED_PRIORITIES_WITH_ORDER = ("UrgentImportant", "NotUrgentImportant", "UrgentNotImportant", "NotUrgentNotImportant")

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
            print(e.message)

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
            print(e.message)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        try:
            if not isinstance(new_status, str) or new_status == "":
                raise TaskFormatException("Task status must be a non-empty string.")
            if new_status not in Task.ALLOWED_STATUSES_WITH_ORDER:
                raise TaskFormatException(
                    """Task priority must be: ToDo, InProgress or Finished."""
                )

            self._status = new_status
        except TaskFormatException as e:
            print(e.message)

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date):
        try:
            if (not isinstance(new_due_date, str)
                    or new_due_date == ""
                    or not re.match(r"^\d{4}-\d{2}-\d{2}$", new_due_date)
            ):
                raise DataFormatException("Task due date must be a non-empty string in a format: YYYY-MM-DD.")

            self._due_date = new_due_date
        except TaskFormatException as e:
            print(e.message)

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

    def __str__(self):
        return (f"{self._name},"
                f" priority={self._priority},"
                f" status={('Do zrobienia 📝' if self._status == Task.ALLOWED_STATUSES_WITH_ORDER[0]
                            else 'W trakcie ⏳' if self._status == Task.ALLOWED_STATUSES_WITH_ORDER[1]
                else 'Zakończone ✅' if self._status == Task.ALLOWED_STATUSES_WITH_ORDER[2] else self._status)},"
                f" due_date={self._due_date},"
                f" category={self._category},"
                f" description={self._description}")
