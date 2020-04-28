from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QStyle, QDesktopWidget 
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
import sys
import os
import json
import csv 
from PyQt5.QtCore import Qt 

class TaskTimer(QtWidgets.QMainWindow):

    def __init__(self):
        super(TaskTimer, self).__init__()
  
        topmost_folder = os.path.basename( os.getcwd() )
        if topmost_folder == 'task_timer':
            base_path = os.getcwd()
        elif topmost_folder == 'dist':
            base_path = os.path.dirname( os.getcwd()  )
        else:
            print('error, folder structure not recognized') 

        log_elsewhere = True   
        if log_elsewhere:
            self.log_dir = 'D:\Mijn_documenten\Dropbox\D_notebook\log_files'
        else:
            self.log_dir = os.path.join(base_path,'log_files')

        # load currently stored task labels 
        self.label_filename = os.path.join( self.log_dir, 'label_options.json' )
        with open(  self.label_filename , 'r') as f:  
             self.labelOptions = json.load(f)    
  
        uic.loadUi( os.path.join(base_path, "task_timer_layout.ui"), self)#currency_converter  

        for label in  self.labelOptions: 
            self.comboBoxLabel.addItem(label)   
 
        test_mode = False
        if test_mode:
            self.max_time =  QtCore.QTime(0, 0, 15)
            self.red_time =  QtCore.QTime(0, 0, 10)
            y_offset = 300
        else:
            self.max_time =  QtCore.QTime(0, 25, 0)
            self.red_time =  QtCore.QTime(0, 2, 0)
            y_offset = 100

         # set screen geometry
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 125
        dy = 130 
        self.setWindowTitle('Task Timer')
        self.setGeometry(sw-dx,sh-dy-y_offset,dx,dy) 

        self.setWindowFlags(Qt.WindowStaysOnTopHint)  
        self.setWindowFlag(Qt.FramelessWindowHint)  
 
        # boolean to have different timing parameters for testing 
        self.time = self.max_time  
        self.lineEditTime.setText(self.time.toString("mm:ss")) 
 
        self.timer = QtCore.QTimer()  
        self.timer.timeout.connect(self.lineEditTimerEvent) 
 
        self.pushButtonPlayPause.clicked.connect(self.onPlayPause)
        self.pushButtonStop.clicked.connect(self.onStop)

        self.pushButtonStop.setIcon( self.style().standardIcon(QStyle.SP_MediaStop))
        self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def lineEditTimerEvent(self): 

        if self.time == self.max_time:

            self.t0 = QtCore.QTime.currentTime().toString("hh:mm:ss") 
            self.date = QtCore.QDate.currentDate()

            day_delta = self.date.dayOfWeek()
            monday_date = self.date.addDays(-day_delta+1).toString("yyyy_MM_dd")

            self.log_filename = os.path.join( self.log_dir, 
                                        'task_log_'+ monday_date +'.csv' ) 
            # read and append label 
            self.labelBoxText = self.comboBoxLabel.currentText() 
            if self.labelBoxText not in self.labelOptions:
                if len(self.labelBoxText)>18:
                    label_cropped = self.labelBoxText[:18]
                else:
                    label_cropped = self.labelBoxText

                self.labelOptions.append( label_cropped )

                # add new label option to dict 
                with open(self.label_filename, 'w') as outfile:
                    json.dump(self.labelOptions, outfile)      
                    print("Adding label to files")
 
        self.time = self.time.addSecs(-1) 

        self.lineEditTask.setEnabled(False)
        self.comboBoxLabel.setEnabled(False) 



        if self.time == QtCore.QTime(0, 0, 0): 
            self.append_list_as_row()   
            self.time = self.max_time
 
        self.lineEditTime.setText(self.time.toString("mm:ss")) 
        self.setColor()
 
    def onPlayPause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay))

        else: 
            self.timer.start(1000)
            self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPause))

             
    def onStop(self):
        self.timer.stop()
        self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay))

        if self.time < self.max_time:
            self.append_list_as_row()    

        self.time = self.max_time 
        self.lineEditTime.setText(self.time.toString("mm:ss")) 
        self.setColor()

        self.lineEditTask.setEnabled(True)
        self.comboBoxLabel.setEnabled(True) 


    def setColor(self):    
        p = self.palette() 
        if self.time < self.red_time: 
            total_sec = float(self.red_time.second()+60*self.red_time.minute()) 
            red_sec = float(self.time.second()+60*self.time.minute())
            ratio = 1-red_sec/total_sec
            r = int(255)
            g = int(255-ratio*220)
            b = int(255-ratio*220) 
            p.setColor(self.backgroundRole(), QColor(r,g,b)  )  
        else:
            p.setColor(self.backgroundRole(), QColor(242,242,242)   )  
        self.setPalette(p)

    def append_list_as_row(self): 
        output_list= [self.date.toString("yyyy/MM/dd"), 
            self.t0, 
            self.lineEditTask.text(), 
            self.labelBoxText,
           (self.max_time.minute()*60+self.max_time.second()) - (self.time.minute()*60 + self.time.second())
            ]    
        fileHeader = [ "date","start time","Task","Label","Duration (s)"]
        if not os.path.exists(self.log_filename):
            bool_add_header = True
        else:
            bool_add_header = False 
        with open(self.log_filename, 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj) 
            if bool_add_header:
                csv_writer.writerow( fileHeader) 
            csv_writer.writerow(output_list) 
  
def main():  
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  
    win = TaskTimer()
    win.show()
    sys.exit(app.exec()) 

if __name__ == '__main__':
    main()  