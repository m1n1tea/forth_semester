from calculatorlogic import *
from PyQt6 import uic
from PyQt6.QtWidgets import *
from enum import * 

def to_base(number, base):
    base_string = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while number:
        result += base_string[number % base]
        number //= base
    return result[::-1] or "0"

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
    
    def top(self) -> Command | None:
        if len(self.__commands) > 0:
            return self.__commands[-1]
        return None
    
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
        if (digit >= self.base):
            return
        self.setText(Command.separateNumber(Command.lStripZero(self.__line.text() + str(digit))))
        
    def setText(self, text: str):
        #if text.isdigit():
          #  self.original_number_in_base_10 = int(text)
        self.__line.setText(text)
     
    def clear(self):
        self.setText("0")

    def changeBase(self, new_base: int):
       self.base = new_base
       self.__line.setText(to_base(int(self.original_number_in_base_10), self.base))
        
    def getText(self) -> str:
        return self.__line.text()

    __line : QLabel = None
    original_number_in_base_10 : int = 0
    base : int = 10


class NumberSystemLine(CommandLine):
    def setText(self, text: str):
        self.current_number_system = int(text)
        return super().setText(self.template + text)
    template: str = "Number System: "
    current_number_system: int = 10


commandHistory : CommandHistory = CommandHistory()
mainCommandLine : CommandLine = CommandLine()
historyCommandLine : CommandLine = CommandLine()
numberSystemLine : NumberSystemLine = NumberSystemLine()

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
        #mainCommandLine.clear()

    def get(self):
        return self.__currentOperation.value
    
    __currentOperation : PossibleOperation = None
    
# Placeholder
def calculate(something: str) -> str:
    return something

class BackspaceCommand(Command):
    def __init__(self, something):
        self.changeTo(something)

    def changeTo(self, other: str) -> None:
        if not mainCommandLine.isEmpty():
            mainCommandLine.setText(mainCommandLine.getText()[0:-1])
            if mainCommandLine.isEmpty():
                mainCommandLine.setText("0")
        super().changeTo(other)
    
    def get(self):
        return 


class EqualCommand(Command):
    def __init__(self, operation):
        self.changeTo(operation)

    def changeTo(self, other: str) -> None:
        if not mainCommandLine.isEmpty():
            OperationQueue.appendToQueue(str(mainCommandLine.original_number_in_base_10) + self.get())
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
        mainCommandLine.changeBase(mainCommandLine.base)
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
        elif command == "⌫":
            return BackspaceCommand(command)

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
numberSystemLine.setLabel(findChildOfAName(form.whole_calculator, QLabel, "label"))


buttonLayout : QGridLayout = findChildOfAName(form.whole_calculator, QWidget, "buttons").layout()

def onSliderValueChange(new_value: str):
    numberSystemLine.setText(new_value)
    mainCommandLine.changeBase(int(new_value))
    if buttonLayout is None:
        return
    for row_index in range(buttonLayout.rowCount()): 
        for column_index in range(buttonLayout.columnCount() + 2):
            if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
                button = buttonLayout.itemAtPosition(column_index, row_index).widget()
                if isinstance(button, QPushButton) and not button.text().isdigit():
                    continue
                if isinstance(button, QPushButton) and int(button.text()) < int(new_value):
                    button.setDisabled(False)
                    button.setStyleSheet("background-color: gray")
                elif int(button.text()) > int(new_value):
                    button.setEnabled(True)
                    

slider : QSlider = findChildOfAName(form.whole_calculator, QSlider, "horizontalSlider")
slider.valueChanged.connect(lambda : onSliderValueChange(str(slider.value())))

for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount() + 2):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, text=button.text(): CommandFactory.constructFromString(text))

print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
