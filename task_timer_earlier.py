from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QStyle, QDesktopWidget 
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

import sys
import os
import json
import csv 

import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

# load project functions
package_path = 'D:\code_projects\\task_timer'
sys.path.append(package_path)
import analyze_log_functions as alf


class Second(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        uic.loadUi(r"D:\\code_projects\\task_timer\\todo_window_gui.ui",self)   
        self.fileNameDropbox = 'D:\\Mijn_documenten\Dropbox\\daily_notes_dropbox.txt'
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 125
        dy = 100
        y_offset = 235
        # y_offset = 635 
        self.setWindowTitle('Dropbox todo') 
        self.setGeometry(sw-dx,sh-dy-y_offset,dx,dy) 

        self.setWindowFlag(Qt.FramelessWindowHint)   
        self.textEditDropbox.setReadOnly(True) 
        self.readDropbox() 
    def readDropbox(self): 
        with open( self.fileNameDropbox, 'r',encoding="utf8") as reader:  
            try:
                self.data = reader.read()
            except:
                self.data = 'invalid dropbox entry' 
        self.textEditDropbox.setText( self.data )   




class TaskTimer(QtWidgets.QMainWindow):

    def __init__(self):
        super(TaskTimer, self).__init__() 

        topmost_folder = os.path.basename( os.getcwd() )
        if topmost_folder == 'task_timer':
            base_path = os.getcwd()
        elif topmost_folder == 'dist':
            base_path = os.path.dirname( os.getcwd()  )
        else:
            base_path = r'D:\code_projects\task_timer'
            print('error, folder structure not recognized') 
            
        #------------------------------------------------------
        self.log_elsewhere = True
        #------------------------------------------------------ 

        if self.log_elsewhere:
            self.log_dir = 'D:\Mijn_documenten\Dropbox\D_notebook\log_files'
        else:
            self.log_dir = os.path.join(base_path,'log_files')
 
        self.fig_dir = os.path.join(base_path,'figs')

        # load currently stored task labels 
        self.config_filename = os.path.join( self.log_dir, 'task_timer_config.json' )
        with open(  self.config_filename , 'r') as f:  
             self.config = json.load(f)     

        uic.loadUi( os.path.join(base_path, "task_timer_layout.ui"), self)#currency_converter  

        for label in  self.config["labels"]: 
            self.comboBoxLabel.addItem(label)   
 
        if self.config["test_mode"]  :
            self.max_time =  QtCore.QTime(0, 0, 15) 
            self.red_time =  QtCore.QTime(0, 0, 10)
            y_offset = 500
        else:
            self.max_time =  QtCore.QTime(0, self.config["task_minutes"], 0)
            self.red_time =  QtCore.QTime(0, self.config["red_minutes"], 0)
            y_offset = 100

         # set screen geometry
        screenGeom = QDesktopWidget().availableGeometry() 
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 125
        dy = 130 
        self.top = sh-y_offset
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
        self.pushButtonPlot.clicked.connect(self.onPlot)

        self.pushButtonStop.setIcon( self.style().standardIcon(QStyle.SP_MediaStop))
        self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay)) 
        self.pushButtonPlot.setIcon(QtGui.QIcon(  os.path.join( self.fig_dir, 'graph_icon.ico' ) ))
        self.pushButtonPlot.setIconSize(QtCore.QSize(24,24))
 
        self.dialog = Second(self) 

        self.lineEditTimerEvent2() 

        self.timer2 = QtCore.QTimer()  
        self.timer2.timeout.connect(self.lineEditTimerEvent2) 
        self.timer2.start(5000)  

    def lineEditTimerEvent2(self):    
        try:
            self.dialog.readDropbox()
        except:
            print('issue reading data')  
        if len(self.dialog.data) > 1:
            self.dialog.show() 
        else:
            self.dialog.hide()  

 


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
            if self.labelBoxText not in self.config["labels"]:
                if len(self.labelBoxText)>18:
                    label_cropped = self.labelBoxText[:18]
                else:
                    label_cropped = self.labelBoxText

                self.config["labels"].append( label_cropped )
 
                # add new label option to dict  
                with open(self.config_filename, 'w') as outfile:
                    json.dump(self.config, outfile, indent=2)      
                    print("Adding label to config file")
   
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
        print('stopped') 
        self.timer.stop()
        self.pushButtonPlayPause.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay))

        if self.time < self.max_time:
            self.append_list_as_row()    

        self.time = self.max_time 
        self.lineEditTime.setText(self.time.toString("mm:ss")) 
        self.setColor()

        self.lineEditTask.setEnabled(True)
        self.comboBoxLabel.setEnabled(True) 


    def onPlot(self):  
        if len(plt.get_fignums()) ==0: 
            # make colorscheme 
            cols = np.array([
            [31,120,180], 
            [178,223,138], 
            [227,26,28], 
            [255,127,0], 
            [202,178,214], 
            [106,61,154], 
            [255,255,153],
            [51,160,44], 
            [251,154,153], 
            [253,191,111], 
            [166,206,227]
            ]) /255  

            # load most recent log file   
            log_files = sorted(glob.glob( self.log_dir+ os.path.sep + '*.csv'))  

            df= pd.read_csv( log_files[-1], index_col=None, header=0)   
             
            # remove any task shorter than 1 minute, it's probably originated from a test
            bool_short_duration = df['Duration (s)'] < 60
            df = df[~bool_short_duration]

            # modify data to useful format 
            df['date'] = pd.to_datetime(df['date'] )  
            df['Duration (hh:mm:ss)'] = pd.to_timedelta(df['Duration (s)'],'s') 
 

            if not df.empty:
                # find unique labels for color mapping
                labels = df['Label'].unique()     
                label_dict = {}
                for label,col in zip(labels,cols): 
                    label_dict[label] = col  

                # plot figure  
                fig, ax = plt.subplots(2, 2, squeeze=False, figsize =(10,5))
     
                alf.plot_week_tasks( ax[0,0], df, label_dict ) 
                alf.plot_time_spent_weekly( ax[0,1], df, label_dict  )
                alf.plot_time_spent_daily( ax[1,0], df, label_dict  ) 
                alf.plot_week_text(ax[1,1], df, self.config["select_labels"], 'Time worked')
                    
                plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.4, hspace=None)   
                plt.show( ) 
        else:  
            plt.close()   

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