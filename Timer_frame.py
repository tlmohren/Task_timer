#!/usr/bin/env python3

# Filename: pycalc.py

"""PyCalc is a simple calculator built using Python and PyQt5."""

import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout 
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget

from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime, QDate
 
import datetime 
import time


# Create a subclass of QMainWindow to setup the calculator's GUI
class PyPomodoro(QMainWindow): 

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second 

    def showTime(self):
        # currentTime = QTime.currentTime()
        # displayTxt = currentTime.toString('hh:mm:ss')  
 
        now = QTime.currentTime() 
        numOfSeconds = self.t0.secsTo( now ) 
        countDown = 25*60 - numOfSeconds
        displayTxt = time.strftime('%M:%S', time.gmtime(countDown))
 
        self.display.setText(displayTxt)

    def _createButtons(self): 
        # layout = QVBoxLayout()
        self.generalLayout.addWidget(QPushButton('Start'))
        self.generalLayout.addWidget(QPushButton('Pauze'))
        self.generalLayout.addWidget(QPushButton('Stop'))
        # self.setLayout(layout)
   
    def createTextbox(self):
        # self.textbox = QLineEdit(self)
        self.generalLayout.addWidget(  QLineEdit('Task') )
        self.generalLayout.addWidget(  QLineEdit('Label') )












    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties

        # keep window on top at all times
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # set screen geometry
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx =200
        dy = 500 
        self.setWindowTitle('PyQt5 App') 
        self.setWindowTitle('PyPomodoro')
        self.setGeometry(sw-dx,sh-dy,dx,dy) 
        self.setFixedSize( dx,dy)



        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)


        # Create the display and the buttons
        self.createTextbox()
        self._createDisplay()
        self._createButtons()


        # startup time
        self.t0 = QTime.currentTime()  
        print( self.t0.toString('hh:mm:ss') )  
 


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyPomodoro()
    view.show()
    # Execute the calculator's main loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()