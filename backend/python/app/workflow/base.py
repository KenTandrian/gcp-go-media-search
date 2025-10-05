from abc import ABC, abstractmethod
from typing import Any, Dict

class Context:
    """A simple context object to pass data between commands."""
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self.errors: Dict[str, Exception] = {}

    def set(self, key: str, value: Any):
        self._data[key] = value

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def add_error(self, command_name: str, error: Exception):
        self.errors[command_name] = error

    def has_errors(self) -> bool:
        return bool(self.errors)

class Command(ABC):
    """Abstract base class for a command in the Chain of Responsibility."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, context: Context):
        """The core logic of the command."""
        pass

    def is_executable(self, context: Context) -> bool:
        """Determines if the command can be executed."""
        return True

class Chain:
    """Represents a chain of commands to be executed in sequence."""
    def __init__(self, name: str):
        self.name = name
        self.commands: list[Command] = []

    def add_command(self, command: Command):
        self.commands.append(command)

    def execute(self, context: Context):
        """Executes the commands in the chain sequentially."""
        for command in self.commands:
            if command.is_executable(context):
                try:
                    command.execute(context)
                except Exception as e:
                    context.add_error(command.name, e)
            
            if context.has_errors():
                print(f"Chain '{self.name}' halted at command '{command.name}' due to errors.")
                break
