from PyQt6 import uic
from PyQt6.QtWidgets import *
from enum import * 


class Command:
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

class DigitCommand(Command): 
    def __init__(self):
        pass
    def __init__(self, default):
        self.changeTo(default)

    def changeTo(self, other: int):
        self.number = other
       # self.commandLine.setText(Command.separateNumber(Command.lStripZero(self.commandLine.text() + str(self.number))))

    
    def get(self) -> int: 
        return self.number
    
    number : int = 0
   
class OperationCommand(Command):
    def __init__(self):
        pass
    def __init__(self, operation):
        self.changeTo(operation)

    @staticmethod 
    def checkIfPossible(operation: str) -> bool:
        operations = {"+", "-", "/", "*"}
        return operation in operations
    
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
    
class CommandFactory:
    @staticmethod
    def constructFromString(command: str) -> Command:
        if command.isdigit():
            return DigitCommand(int(command))
        elif OperationCommand.checkIfPossible(command):
            return OperationCommand(command)
        elif command == "C":
            return ClearCommand()

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

def findChildOfAName(parent, type, name: str):
    children = parent.findChildren(type)
    for i in range(len(children)):
        if children[i].objectName() == name:
            return children[i]
    return None

buttonLayout : QGridLayout = findChildOfAName(form.whole_calculator, QWidget, "buttons").layout()

#findChildOfAName(form.whole_calculator, QLabel, "result")
current_command: Command = CommandFactory.constructFromString("0")


for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount() + 2):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, text=button.text(): print(type(CommandFactory.constructFromString(text))))

print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
