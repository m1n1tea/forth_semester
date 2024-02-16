import calculatorlogic
from calculatorlogic import *
from PyQt6 import uic
from PyQt6.QtWidgets import *
from enum import * 

from PyQt6.QtGui import QKeySequence, QKeyEvent, QShortcut
from PyQt6 import QtCore


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
        self.setText(Command.separateNumber(Command.lStripZero(self.__line.text() + str(digit))))
        
    def setText(self, text: str):
        self.__line.setText(text)
     
    def clear(self):
        self.setText("0")

    def changeBase(self, new_base: int):
        calculator_logic.input_number_system(new_base)
        self.base = new_base
        self.__line.setText(calculator_logic.get_main_fraction())
        
    def getText(self) -> str:
        return self.__line.text()

    __line : QLabel = None
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
    digitsAfter9={"a", "b", "c", "d", "e", "f"}

    @staticmethod
    def checkIfAvailable(command:str) -> bool:
        for i in range(len(command)):
            if not (command[i].isdigit() or command[i] in DigitCommand.digitsAfter9):
                return False
        return True
    
    def __init__(self):
        pass
    def __init__(self, default):
        self.changeTo(default)

    def changeTo(self, other:str):
        self.number = int(other, numberSystemLine.current_number_system)
        mainCommandLine.appendDigit(other)
        super().changeTo(other)
        calculator_logic.input_number(mainCommandLine.getText())
       
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
        print(mainCommandLine.getText())
        calculator_logic.input_number(mainCommandLine.getText())
        calculator_logic.input_operator(other)
        OperationQueue.appendToQueue(str(mainCommandLine.getText()) + self.get())
        historyCommandLine.setText(OperationQueue.queue)
        mainCommandLine.clear()

    def get(self):
        return self.__currentOperation.value
    
    __currentOperation : PossibleOperation = None
    
# Placeholder
def calculate(something: str) -> str:
    return calculator_logic.get_main_fraction()

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
        calculator_logic.input_number(mainCommandLine.getText())
        calculator_logic.input_operator('=')
        if not mainCommandLine.isEmpty():
            OperationQueue.appendToQueue(str(mainCommandLine.getText()) + self.get())
        elif not OperationQueue.isEmpty():
            OperationQueue.appendToQueue(self.get())

        # Here we delete a sign if the last command was something of a "+, -, /, *", since we do not
        # want to find something like: "65-=65"
        if isinstance(commandHistory.top(), OperationCommand):
            temp_str = OperationQueue.queue 
            OperationQueue.clearQueue()
            OperationQueue.appendToQueue(temp_str[0:-2] + self.get()) 
        elif isinstance(commandHistory.top(), EqualCommand):
            return      
        
        
        historyCommandLine.setText(OperationQueue.queue)
        mainCommandLine.clear()
        result= calculate(OperationQueue.queue)
        mainCommandLine.setText(result)
        mainCommandLine.changeBase(mainCommandLine.base)
        OperationQueue.clearQueue()
        #OperationQueue.appendToQueue(result)
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
        calculator_logic.input_operator("C")
    
    def get(self):
        return "C"
    
class CommandFactory:
    
    @staticmethod
    def constructFromString(command: str) -> Command:
        if DigitCommand.checkIfAvailable(command.lower()):
            return DigitCommand(command)
        elif OperationCommand.checkIfPossible(command):
            return OperationCommand(command)
        elif command == "Clear":
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

calculator_logic = calculatorlogic.CalculatorLogic()


buttonLayout : QGridLayout = findChildOfAName(form.whole_calculator, QWidget, "buttons").layout()
chars : QHBoxLayout = findChildOfAName(form.whole_calculator, QGroupBox, "horizontalGroupBox").layout()

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
                    button.setEnabled(True)
                    #button.setStyleSheet("background-color: gray")
                elif int(button.text()) >= int(new_value):
                    button.setDisabled(True)
    for i in range (chars.count()):
        button = chars.itemAt(i).widget()
        result = list(DigitCommand.digitsAfter9).index(button.text().lower())
        if (result +  10 < int(new_value)):
            chars.itemAt(5 - result).widget().setEnabled(True)
        else:
            chars.itemAt(5 - result).widget().setEnabled(False)

slider : QSlider = findChildOfAName(form.whole_calculator, QSlider, "horizontalSlider")
slider.valueChanged.connect(lambda : onSliderValueChange(str(slider.value())))

for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount() + 2):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                    
                    if (button.text == "⌫"):
                        # Does not work forsome reason
                        button.shortcut = QShortcut(QtCore.Qt.Key.Key_Backspace, button)
                    else:
                        button.shortcut = QShortcut(QKeySequence(button.text()), button)
                    button.shortcut.activated.connect(lambda text=button.text(): CommandFactory.constructFromString(text))
                    button.clicked.connect(lambda checked, text=button.text(): CommandFactory.constructFromString(text))

for i in range (chars.count()):
    button = chars.itemAt(i).widget()
    button.shortcut = QShortcut(QKeySequence(button.text().lower()), button)
    button.shortcut.activated.connect(lambda text=button.text(): CommandFactory.constructFromString(text))
    button.clicked.connect(lambda checked, text=button.text(): CommandFactory.constructFromString(text))
    button.setDisabled(True)

print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
