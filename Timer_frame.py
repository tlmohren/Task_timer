#!/usr/bin/env python3

# Filename: pydoro.py
 
import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
import PyQt5.QtWidgets
from PyQt5 import QtWidgets, QtGui

import os 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout 
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget

from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime, QDate

from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu
from PyQt5.QtGui import QIcon

import functools 
import datetime 
import time 
import csv

 
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
 
# Create a subclass of QMainWindow to setup the calculator's GUI
class PyPomodoro(QMainWindow):  
    QMainWindow.n_sec = 25*60
    QMainWindow.pause = True
    QMainWindow.countDown = QMainWindow.n_sec

    QMainWindow.taskboxText = 'empytTask'
    QMainWindow.lineboxText = 'emptyLabel'
    QMainWindow.date = QDate.currentDate().toString("dd/MM/yyyy") 
    QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss') 
  
    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        font = self.display.font()
        font.setPointSize(30)
        self.display.setFont( font)      # set font
 
                # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second 

    def showTime(self):
        # currentTime = QTime.currentTime()
        # displayTxt = currentTime.toString('hh:mm:ss')  
 
        if (QMainWindow.pause == False) & (QMainWindow.countDown>0): 
            QMainWindow.countDown = QMainWindow.countDown - 1
            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown))
        #     print(self.pause) 
        elif (QMainWindow.pause == True): 
            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown))
        else:
            print('reset time')
            QMainWindow.pause = True 
            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown)) 
            print('log countdown')
 
            output_list= [QMainWindow.date, 
                QMainWindow.t0, 
                QMainWindow.taskboxText, 
                QMainWindow.lineboxText,
                str(QMainWindow.n_sec - QMainWindow.countDown)]  
            append_list_as_row('task_log.csv', output_list) 
            # print(QMainWindow.date, QMainWindow.t0, QMainWindow.task, QMainWindow.label, QMainWindow.n_sec - QMainWindow.countDown)

            print( output_list)
            QMainWindow.countDown = QMainWindow.n_sec

        self.display.setText(displayTxt)
 
    def _createButtons(self):  
        def press_start(self):    
            if QMainWindow.countDown == QMainWindow.n_sec:
                QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss')  
                QMainWindow.taskboxText= taskbox.text()
                QMainWindow.lineboxText= linebox.text()
                print(QMainWindow.taskboxText, QMainWindow.lineboxText)
            QMainWindow.pause = False 

        def press_pause(self):  
            btn.setText("Start")
            QMainWindow.pause = True  
 
        def press_stop():  
            stp.setText("Stop") 
            btn.setText("Start") 
            print('log countdown') 
            output_list= [QMainWindow.date, 
                QMainWindow.t0, 
                QMainWindow.taskboxText, 
                QMainWindow.lineboxText,
                str(QMainWindow.n_sec - QMainWindow.countDown)]  
            append_list_as_row('task_log.csv', output_list) 
            print( output_list)


            QMainWindow.countDown = QMainWindow.n_sec#25*60 
            QMainWindow.pause = True  


 
        taskbox = QLineEdit( )
        # textboxValue= taskbox.text() 
        self.generalLayout.addWidget( taskbox   )
  
        linebox = QLineEdit( )
        # textboxValue= linebox.text() 
        self.generalLayout.addWidget( linebox   )
 
        btn = QPushButton('Start',self)
        btn.clicked.connect( press_start )  # Connect clicked to press_start()
        self.generalLayout.addWidget( btn )
 
        pau = QPushButton('Pause')
        pau.clicked.connect( press_pause)  # Connect clicked to press_start()
        self.generalLayout.addWidget( pau)


        stp = QPushButton('Stop')
        stp.clicked.connect( press_stop)  # Connect clicked to press_start()
        self.generalLayout.addWidget( stp )
  

    def createTextbox(self):
        # self.textbox = QLineEdit(self)
        # tsk = QLineEdit('Task')
        # btn.clicked.connect( press_start ) 
        self.generalLayout.addWidget( QLineEdit('Emptry1') )





 

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties

        # keep window on top at all times
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
    
        # first attempt at transparency 
        self.setWindowOpacity(0.9)


        # this will hide the title bar 
        self.setWindowFlag(Qt.FramelessWindowHint)  

        # change tray icon 
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'tomato.png'))  
 
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        picture_loc = scriptDir + os.path.sep + 'tomato.png' 
        self.setWindowIcon(QIcon( picture_loc) )
        # win.setWindowIcon (QIcon('logo.png'))

        # set screen geometry
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 130
        dy = 200 
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
        self._createDisplay()
        self._createButtons()
        # not used currently 
        # self.createTextbox() 
 


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    pydoro = QApplication(sys.argv) 
    pydoro.setStyle('Fusion')  
    # Show the calculator's GUI
    view = PyPomodoro()
    view.show()

    # Execute the calculator's main loop
    sys.exit(pydoro.exec_())

if __name__ == '__main__':
 
    main()

