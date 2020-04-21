#!/usr/bin/env python3

# Filename: task_timer.py
  
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt 

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDesktopWidget 
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QStyle 

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon 
 
import datetime 
import time 
import sys
import csv 
import json
import os  
 
def append_list_as_row(file_name, list_of_elem):

    fileHeader = [ "date","start time","Task","Label","Duration (s)"]

    if not os.path.exists(file_name):
        bool_add_header = True
    else:
        bool_add_header = False 

    with open(file_name, 'a+', newline='') as write_obj:

        csv_writer = csv.writer(write_obj)

        # if it's the first line, add the header
        if bool_add_header:
            csv_writer.writerow( fileHeader)

        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
 
# Create a subclass of QMainWindow to setup the calculator's GUI
class Timer_Class(QMainWindow):  

	# boolean to have different timing parameters for testing 
    test_mode = False
    log_elsewhere = True

    if test_mode == False:
        QMainWindow.n_sec = 25*60
        QMainWindow.red_seconds = 60
    else:
        QMainWindow.n_sec = 15
        QMainWindow.red_seconds = 10

    # boolean to see if 
    QMainWindow.pause = True
    QMainWindow.stbutton_bool = True
    QMainWindow.countDown = QMainWindow.n_sec

    QMainWindow.taskboxText = 'empytTask'
    QMainWindow.labelboxText = 'Other' 

    # find current date 
    QMainWindow.date = QDate.currentDate().toString("yyyy/MM/dd") 

    # initialize time of start script (will be overwritten when play is pressed) 
    ## is initialization necessary? 
    QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss')  

    # find folder with logs and json files
    topmost_folder = os.path.basename( os.getcwd() )
 
     # find base foder, is executable located in folder structure? 
    if topmost_folder == 'task_timer':
        base_path = os.getcwd()
    elif topmost_folder == 'dist':
        base_path = os.path.dirname( os.getcwd()  )
    else:
        print('error, folder structure not recognized')

    # create directory of log files 
    QMainWindow.log_dir = os.path.join(base_path,'log_files')
    today = datetime.date.today()
    date_Monday = today - datetime.timedelta(days=today.weekday()) 

    if log_elsewhere:
        QMainWindow.log_filename = os.path.join('D:\Mijn_documenten\Dropbox\D_notebook\log_files',
            'taskLog_'+ datetime.datetime.strftime(date_Monday,  "%Y_%m_%d") +'.csv')
    else:
        QMainWindow.log_filename = os.path.join( QMainWindow.log_dir, 
                                'taskLog_'+ datetime.datetime.strftime(date_Monday,  "%Y_%m_%d") +'.csv' )
 
    # load currently stored task labels 
    QMainWindow.label_filename = os.path.join( QMainWindow.log_dir, 'label_options.json' )
    
    with open(  QMainWindow.label_filename , 'r') as f:  
         QMainWindow.labelOptions = json.load(f)   

    def _createDisplay(self):
        """Create the display."""

        # Create the display widget
        self.display = QLineEdit()
 
        self.display.setAlignment(Qt.AlignRight) 
        self.display.setReadOnly(True)

        font = self.display.font()
        font.setPointSize(30)
        self.display.setFont( font)      # set font
 
        # Add the display to the general layout 
        self.grid.addWidget(self.display,0,0,1,2) 
 
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second 

    def showTime(self): 
        if (QMainWindow.pause == False) & (QMainWindow.countDown>0): 
            QMainWindow.countDown = QMainWindow.countDown - 1
            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown)) 

            if (QMainWindow.countDown < QMainWindow.red_seconds): 
                p = self.palette() 

                ratio = 1-QMainWindow.countDown /QMainWindow.red_seconds
                r = int(255)
                g = int(255 - ratio*220)
                b = int(255 - ratio*220) 
                p.setColor(self.backgroundRole(), QColor(r,g,b)  )  
                self.setPalette(p)
            else:
                p = self.palette() 
                p.setColor(self.backgroundRole(), self.backGroundColor  )  
                self.setPalette(p)
 
        elif (QMainWindow.pause == True): 
            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown))

            if (QMainWindow.countDown > QMainWindow.red_seconds):
                p = self.palette() 
                p.setColor(self.backgroundRole(), self.backGroundColor )  
                self.setPalette(p)
 
        else: 
            p = self.palette() 
            p.setColor(self.backgroundRole(), self.backGroundColor )  
            self.setPalette(p) 

            displayTxt = time.strftime('%M:%S', time.gmtime(QMainWindow.countDown))  
 
            output_list= [QMainWindow.date, 
                QMainWindow.t0, 
                QMainWindow.taskboxText, 
                QMainWindow.labelboxText,
                str(QMainWindow.n_sec - QMainWindow.countDown)]  

            append_list_as_row( QMainWindow.log_filename , output_list)  

            QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss') 
            QMainWindow.countDown = QMainWindow.n_sec 

        self.display.setText(displayTxt)
  

    def _createLabelBoxes(self):  
        empty = True

    def _createButtons(self):  

        def press_start_pause(self):     
            if QMainWindow.stbutton_bool: 
                # turn pause off so that timer is running 
                QMainWindow.pause = False 

                # start button is false 
                QMainWindow.stbutton_bool = False

                # turn button into pause button  
                stpau.setIcon( stpau.style().standardIcon(QStyle.SP_MediaPause))
 
                # if this is start when timer is at max timer, then store starting properties
                if QMainWindow.countDown == QMainWindow.n_sec:
                    QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss')  
                    QMainWindow.taskboxText= taskbox.text() 
                    QMainWindow.labelboxText = labelbox.currentText()
     
                    if QMainWindow.labelboxText not in QMainWindow.labelOptions:
                        if len(QMainWindow.labelboxText)>18:
                            label_cropped = QMainWindow.labelboxText[:18]
                        else:
                            label_cropped = QMainWindow.labelboxText 
                        QMainWindow.labelOptions.append( label_cropped )
                        labelbox.addItem( label_cropped )    

                        # add new label option to dict 
                        with open(QMainWindow.label_filename, 'w') as outfile:
                            json.dump(QMainWindow.labelOptions, outfile)    

            elif not QMainWindow.stbutton_bool: 
                stpau.setIcon( stpau.style().standardIcon(QStyle.SP_MediaPlay))
                QMainWindow.pause = True
                QMainWindow.stbutton_bool = True
                
        def press_stop():   

            output_list= [QMainWindow.date, 
                QMainWindow.t0, 
                QMainWindow.taskboxText, 
                QMainWindow.labelboxText,
                str(QMainWindow.n_sec - QMainWindow.countDown)]  
            append_list_as_row( QMainWindow.log_filename, output_list)  

            QMainWindow.t0 = QTime.currentTime().toString('hh:mm:ss')  
            QMainWindow.countDown = QMainWindow.n_sec#25*60 
            QMainWindow.pause = True  
            QMainWindow.stbutton_bool = True
            stpau.setIcon( stpau.style().standardIcon(QStyle.SP_MediaPlay)) 

        taskbox = QLineEdit( ) 
        self.grid.addWidget( taskbox,1,0,1,2)
  
        labelbox = QComboBox(self)
        labelbox.setEditable(True)
        for label in  QMainWindow.labelOptions:
            labelbox.addItem(label)   
        self.grid.addWidget(labelbox,2,0,1,2)

        stpau = QPushButton()
        stpau.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay))
        stpau.clicked.connect( press_start_pause) 
  
        stp = QPushButton()
        stp.setIcon( self.style().standardIcon(QStyle.SP_MediaStop))
        stp.clicked.connect( press_stop) 
 
        self.grid.addWidget( stpau,3,0 )
        self.grid.addWidget( stp,3,1 )



  
    def __init__(self):
        """View initializer of Timer_class."""
        super().__init__()

        # keep window on top at all times
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
    
        # first attempt at transparency 
        self.setWindowOpacity(0.9)
 
        # # this will hide the title bar 
        self.setWindowFlag(Qt.FramelessWindowHint)  

        # set screen geometry
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 127
        dy = 160  
        y_offset = 100
        self.setWindowTitle('Task Timer')
        self.setGeometry(sw-dx,sh-dy-y_offset,dx,dy)  

        # set background color
        self.setAutoFillBackground(True)
        self.backGroundColor = QColor(242,242,242) 
        p = self.palette() 
        p.setColor(self.backgroundRole(),  self.backGroundColor ) 
        self.setPalette(p)
 
        # Set the central widget
        # self.verticalLayout = QVBoxLayout()
        self.grid = QGridLayout()
        self._centralWidget = QWidget(self)

        # self._centralWidget.setLayout(self.verticalLayout)
        self._centralWidget.setLayout(self.grid) 

        self.setCentralWidget(self._centralWidget) 

        # Create the display and the buttons
        self._createDisplay()
        self._createLabelBoxes()
        self._createButtons()
  
 
# Client code
def main():
    """Main function."""

    # Create an instance of QApplication
    task_timer = QApplication(sys.argv) 
    task_timer.setStyle('Fusion')  

    # Show the calculator's GUI
    view = Timer_Class()
    view.show()

    # Execute the calculator's main loop
    sys.exit(task_timer.exec_()) 

if __name__ == '__main__':
    main() 