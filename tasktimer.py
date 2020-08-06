#!/home/thomas/Projects/tasktimer/env/bin/python
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from tasktimer import main_window


def main():

    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")
    app_icon = QtGui.QIcon()
    app_icon.addFile("figs/tomato.ico", QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    win = main_window.TaskTimer()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
