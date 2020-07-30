#!/home/thomas/Projects/task_timer/env/bin/python
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import task_timer.main_window as mw


def main():

    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")
    app_icon = QtGui.QIcon()
    app_icon.addFile("figs/tomato.ico", QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    win = mw.TaskTimer()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
