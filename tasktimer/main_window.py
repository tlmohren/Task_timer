from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QStyle, QDesktopWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

import os
import json
import csv
import screeninfo

import matplotlib.pyplot as plt
import matplotlib
import platform
import yaml
import pathlib


from tasktimer import kanban_window
from tasktimer import todo_window
from tasktimer import load_config
from tasktimer import analyze_log_functions


class TaskTimer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        base_path = pathlib.Path(__file__).parent.parent
        file_config = base_path.joinpath("config.yml")

        with open(file_config) as file_config:
            config_all = yaml.load(file_config, Loader=yaml.Loader)

        self.file_config = config_all[platform.node()]

        self.config_dict = load_config.load_config("config.yml")

        with open(self.config_dict["task_config"], "r") as f:
            self.config = json.load(f)

        uic.loadUi(self.config_dict["gui_main"], self)

        for label in self.config["labels"]:
            self.comboBoxLabel.addItem(label)

        if self.config["test_mode"]:
            self.max_time = QtCore.QTime(0, 0, 15)
            self.red_time = QtCore.QTime(0, 0, 10)
            y_offset = 200
        else:
            self.max_time = QtCore.QTime(0, self.config["task_minutes"], 0)
            self.red_time = QtCore.QTime(0, self.config["red_minutes"], 0)
            y_offset = 500

        screenGeom = QDesktopWidget().availableGeometry()
        sh = screenGeom.height()
        sw = screenGeom.width()

        dx = 125
        dy = 130
        self.top = sh - y_offset
        self.setWindowTitle("Task Timer")

        # correct for sidebar if I have only one monitor. Don't really understand why this works though
        n_monitors = len(screeninfo.get_monitors())

        if n_monitors == 1:
            x_base = sw - dx + 100
        else:
            x_base = sw - dx

        self.goal_geometry = [x_base, sh - dy - y_offset, dx, dy]

        self.setGeometry(*self.goal_geometry)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # boolean to have different timing parameters for testing
        self.time = self.max_time
        self.lineEditTime.setText(self.time.toString("mm:ss"))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.lineEditTimerEvent)

        self.pushButtonPlayPause.clicked.connect(self.onPlayPause)
        self.pushButtonStop.clicked.connect(self.onStop)
        self.pushButtonPlot.clicked.connect(self.onPlot)
        self.pushButtonKanban.clicked.connect(self.onKanban)

        self.pushButtonStop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.pushButtonPlayPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.pushButtonPlot.setIcon(
            QtGui.QIcon(str(self.config_dict["fig_dir"].joinpath("graph_icon.ico")))
        )
        self.pushButtonPlot.setIconSize(QtCore.QSize(22, 24))
        self.pushButtonKanban.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogListView)
        )

        self.dialog = todo_window.DropboxWindow()

        self.kanban = kanban_window.KanbanWindow()

        self.lineEditTimerEvent2()

        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.lineEditTimerEvent2)
        self.timer2.start(30000)

    def lineEditTimerEvent2(self):
        try:
            self.dialog.readDropbox()
        except:
            print("issue reading data")
        if len(self.dialog.data) > 1:
            self.dialog.show()
        else:
            self.dialog.hide()

    def lineEditTimerEvent(self):

        if self.time == self.max_time:

            self.t0 = QtCore.QTime.currentTime().toString("hh:mm:ss")
            self.date = QtCore.QDate.currentDate()

            day_delta = self.date.dayOfWeek()
            monday_date = self.date.addDays(-day_delta + 1).toString("yyyy_MM_dd")

            filename = "task_log_" + monday_date + ".csv"
            self.log_filename = self.config_dict["log_dir"].joinpath(filename)

            # read and append label
            self.labelBoxText = self.comboBoxLabel.currentText()
            if self.labelBoxText not in self.config["labels"]:
                if len(self.labelBoxText) > 18:
                    label_cropped = self.labelBoxText[:18]
                else:
                    label_cropped = self.labelBoxText

                self.config["labels"].append(label_cropped)

                # add new label option to dict
                with open(self.config_dict.get("task_config"), "w") as outfile:
                    # with open(self.config_filename, "w") as outfile:
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
            self.pushButtonPlayPause.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

        else:
            self.timer.start(1000)
            self.pushButtonPlayPause.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        self.setGeometry(*self.goal_geometry)
        self.dialog.set_dropbox_geometry()

    def onStop(self):
        self.timer.stop()
        self.pushButtonPlayPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        if self.time < self.max_time:
            self.append_list_as_row()

        self.time = self.max_time
        self.lineEditTime.setText(self.time.toString("mm:ss"))
        self.setColor()

        self.lineEditTask.setEnabled(True)
        self.comboBoxLabel.setEnabled(True)
        self.setGeometry(*self.goal_geometry)
        self.dialog.set_dropbox_geometry()

    def onPlot(self):

        all_figs = matplotlib._pylab_helpers.Gcf.get_all_fig_managers()

        if len(all_figs) == 0:

            cols = self.config_dict["col"]

            file = analyze_log_functions.pick_mostrecent_log(
                self.config_dict["log_dir"]
            )
            df = analyze_log_functions.weekly_data_processing(file)

            if not df.empty:
                # find unique labels for color mapping
                labels = df["Label"].unique()
                label_dict = {}
                for label, col in zip(labels, cols):
                    label_dict[label] = col

                fig, ax = plt.subplots(2, 2, squeeze=False, figsize=(10, 5))

                analyze_log_functions.plot_week_tasks(ax[0, 0], df, label_dict)
                analyze_log_functions.plot_time_spent_weekly(ax[0, 1], df, label_dict)
                analyze_log_functions.plot_time_spent_daily(ax[1, 0], df, label_dict)
                analyze_log_functions.plot_week_text(
                    ax[1, 1], df, self.config["select_labels"], "Time worked"
                )

                fig.subplots_adjust(
                    left=None,
                    bottom=None,
                    right=None,
                    top=None,
                    wspace=0.4,
                    hspace=None,
                )
                fig.show()
        else:
            plt.close("all")
        self.setGeometry(*self.goal_geometry)
        self.dialog.set_dropbox_geometry()

    def onKanban(self):
        if self.kanban.isVisible():
            self.kanban.hide()
            self.kanban.save_state()
        else:
            self.kanban.show()
            self.kanban.update_kanban()
        self.setGeometry(*self.goal_geometry)
        self.dialog.set_dropbox_geometry()

    def setColor(self):
        p = self.palette()
        if self.time < self.red_time:
            total_sec = float(self.red_time.second() + 60 * self.red_time.minute())
            red_sec = float(self.time.second() + 60 * self.time.minute())
            ratio = 1 - red_sec / total_sec
            r = int(255)
            g = int(255 - ratio * 220)
            b = int(255 - ratio * 220)
            p.setColor(self.backgroundRole(), QColor(r, g, b))
        else:
            p.setColor(self.backgroundRole(), QColor(242, 242, 242))
        self.setPalette(p)

    def append_list_as_row(self):
        output_list = [
            self.date.toString("yyyy/MM/dd"),
            self.t0,
            self.lineEditTask.text(),
            self.labelBoxText,
            (self.max_time.minute() * 60 + self.max_time.second())
            - (self.time.minute() * 60 + self.time.second()),
        ]
        fileHeader = ["date", "start time", "Task", "Label", "Duration (s)"]

        if not os.path.exists(self.log_filename):
            bool_add_header = True
        else:
            bool_add_header = False

        with open(self.log_filename, "a+", newline="") as write_obj:
            csv_writer = csv.writer(write_obj)

            if bool_add_header:
                csv_writer.writerow(fileHeader)
            csv_writer.writerow(output_list)
