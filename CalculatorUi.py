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
        commandHistory.push(self)

    def get(self):
        pass

class CommandHistory:         
    def push(self, command: Command):
        self.__commands.append(command)
    
    def top(self) -> Command:
        return self.__commands[-1]
    
    def getCurrentCommand(self) -> Command: 
        return self.top()
    
    # Returns the last command used
    def pop(self) -> Command:
        last_command_used: Command = self.top()
        self.__commands.pop()
        return last_command_used
    
    def debugGetCommands(self):
        return self.__commands
    
    __commands: list[Command] = []


class CommandLine:
    def __init__(self):
        pass

    def isEmpty(self) -> bool:
        return len(Command.lStripZero(self.getText())) == 0
    
    def setLabel(self, label: QLabel):
        self.__line = label
    
    def appendDigit(self, digit: int):
        self.__line.setText(Command.separateNumber(Command.lStripZero(self.__line.text() + str(digit))))
    
    def setText(self, text: str):
        self.__line.setText(text)
     
    def clear(self):
        self.setText("0")

    def getText(self) -> str:
        return self.__line.text()

    __line : QLabel = None


commandHistory : CommandHistory = CommandHistory()
mainCommandLine : CommandLine = CommandLine()
historyCommandLine : CommandLine = CommandLine()

class DigitCommand(Command): 
    def __init__(self):
        pass
    def __init__(self, default):
        self.changeTo(default)

    def changeTo(self, other: int):
        self.number = other
        mainCommandLine.appendDigit(int(other))
        super().changeTo(other)
       
    def get(self) -> int: 
        return self.number
    
    number : int = 0
   
class OperationQueue:
    @staticmethod
    def appendToQueue(text : str):
        OperationQueue.queue += text
    @staticmethod
    def isEmpty() -> bool:
        return len(Command.lStripZero(OperationQueue.queue)) == 0
           
        
    @staticmethod
    def clearQueue():
        OperationQueue.queue = ""
    
    queue : str = ""
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
        super().changeTo(other)
        
        OperationQueue.appendToQueue(mainCommandLine.getText() + self.get())
        historyCommandLine.setText(OperationQueue.queue)
        mainCommandLine.clear()

    def get(self):
        return self.__currentOperation.value
    
    __currentOperation : PossibleOperation = None
    
# Placeholder
def calculate(something: str) -> str:
    return something

class EqualCommand(Command):
    def __init__(self, operation):
        self.changeTo(operation)

    def changeTo(self, other: str) -> None:
        if not mainCommandLine.isEmpty():
            OperationQueue.appendToQueue(mainCommandLine.getText() + self.get())
        elif not OperationQueue.isEmpty():
            OperationQueue.appendToQueue(self.get())

        # Here we delete a sign if the last command was something of a "+, -, /, *", since we do not
        # want to find something like: "65-=65"
        if isinstance(commandHistory.top(), OperationCommand):
            temp_str = OperationQueue.queue 
            OperationQueue.clearQueue()
            OperationQueue.appendToQueue(temp_str[0:-2] + self.get())        
        historyCommandLine.setText(OperationQueue.queue)
        mainCommandLine.clear()
        result : int = calculate("12")
        mainCommandLine.setText(result)
        OperationQueue.clearQueue()
        OperationQueue.appendToQueue(result)
        super().changeTo(other)
    
    def get(self):
        return "="
    
class ClearCommand(Command):
    def __init__(self):
        return self.changeTo(None)
    
    def changeTo(self, other) -> None:
        mainCommandLine.clear()
        historyCommandLine.clear()
        OperationQueue.clearQueue()
    
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
        elif command == "=":
            return EqualCommand(command)

def findChildOfAName(parent, type, name: str):
    children = parent.findChildren(type)
    for i in range(len(children)):
        if children[i].objectName() == name:
            return children[i]
    return None


# Setup
app = QApplication([])

# Cannot annotate types here for some reason
Form, Window = uic.loadUiType("./UI/calculator.ui")

window = Window()
form = Form()
form.setupUi(window)

mainCommandLine.setLabel(findChildOfAName(form.whole_calculator, QLabel, "result"))
historyCommandLine.setLabel(findChildOfAName(form.whole_calculator, QLabel, "previous_input"))

buttonLayout : QGridLayout = findChildOfAName(form.whole_calculator, QWidget, "buttons").layout()

for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount() + 2):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, text=button.text(): CommandFactory.constructFromString(text))

print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
