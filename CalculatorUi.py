from PyQt6 import uic
from PyQt6.QtWidgets import *
from enum import * 


class Command:
    def __init__(self, commandLine : QLabel):
        self.commandLine = commandLine

    @staticmethod
    def lStripZero(number: str) -> str:
        return number.lstrip('0') 

    @staticmethod
    # Repair after
    def separateNumber(number: str) -> str:
        return number
    
    def changeTo(self, other: str) -> None:
        pass

    def get(self):
        pass
    
    commandLine: QLabel = None

class DigitCommand(Command): 
    def changeTo(self, other: int):
        self.number = other
        self.commandLine.setText(Command.separateNumber(Command.lStripZero(self.commandLine.text() + str(self.number))))

    
    def get(self) -> int: 
        return self.number
    
    number : int = 0
   
class OperationCommand(Command):
    class PossibleOperation(Enum):
        NONE = "0"
        ADDITION = "+"
        SUBTRACTION = "-"
        DIVISION = "/"
        MULTIPLICATION = "*"
    
    def changeTo(self, other: str) -> None:
        match other:
            case "+":
                self.__currentOperation = self.PossibleOperation.ADDITION
            case "-":
                self.__currentOperation = self.PossibleOperation.SUBTRACTION
            case "/":
                self.__currentOperation = self.PossibleOperation.DIVISION
            case "*":
                self.__currentOperation = self.PossibleOperation.MULTIPLICATION
            case _:
                raise ValueError(other + " was not one of Possible Operations")

    def get(self):
        return self.__currentOperation.value
    
    __currentOperation : PossibleOperation = None
    
class ClearCommand(Command):
    def changeTo(self, other) -> None:
        return super().changeTo(other)
    
    def get(self):
        return "C"

class CommandHistory: 
    def __init__(self, commandLine: QLabel):
        self.commandLine = commandLine

    def push(self, command: Command):
        self.commands.append(command)
    
    def top(self) -> Command:
        return self.commands[-1]
    
    def getCurrentCommand(self) -> Command: 
        return self.top()
    
    # Returns the last command used
    def pop(self) -> Command:
        last_command_used: Command = self.top()
        self.commands.pop()
        return last_command_used


    commands: list[Command]
    commandLine: QLabel = None


app = QApplication([])

# Cannot annotate types here for some reason
Form, Window = uic.loadUiType("./UI/calculator.ui")


window = Window()
form = Form()
form.setupUi(window)


buttonLayout : QGridLayout = form.buttonLayout

current_command: Command = Command(buttonLayout.itemAtPosition(0, 1).widget())


for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount() + 2):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, text=button.text(): current_command.changeTo(text))

print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
