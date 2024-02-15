from PyQt6 import uic
from PyQt6.QtWidgets import *




class Command: 
    def __init__(self, commandLine : QLabel):
        self.commandLine = commandLine

    def changeTo(self, other: int):
        self.number = other
        self.commandLine.setText(str(self.number))
        
    def get(self) -> int: 
        return self.number
    
    number : int = 0
    commandLine:QLabel = None



app = QApplication([])

# Cannot annotate types here for some reason
Form, Window = uic.loadUiType("./UI/calculator.ui")


window = Window()
form = Form()
form.setupUi(window)


buttonLayout : QGridLayout = form.buttonLayout
current_command: Command = Command(buttonLayout.itemAtPosition(0, 0).widget())

for row_index in range(buttonLayout.rowCount()): 
    for column_index in range(buttonLayout.columnCount()):
        if buttonLayout.itemAtPosition(column_index, row_index) is not None:  
            button = buttonLayout.itemAtPosition(column_index, row_index).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, text=button.text(): current_command.changeTo(text))
print(buttonLayout.rowCount(), buttonLayout.columnCount())
window.show()
app.exec()
print(current_command.get())
