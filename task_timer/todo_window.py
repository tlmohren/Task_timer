from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QStyle, QDesktopWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from . import load_config as lc


class Second(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() | Qt.Dialog)

        self.config_dict = lc.load_config("config.yml")

        uic.loadUi(self.config_dict["gui_name"], self)

        screenGeom = QDesktopWidget().availableGeometry()
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 125
        dy = 100
        y_offset = 235
        self.setWindowTitle("Dropbox todo")
        self.setGeometry(sw - dx + 100, sh - dy - y_offset, dx, dy)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.textEditDropbox.setReadOnly(True)
        tempFont = self.textEditDropbox.font()
        tempFont.setPointSize(8)

        self.textEditDropbox.setFont(tempFont)

        self.readDropbox()

    def readDropbox(self):
        filename = self.config_dict["dropbox_file"]

        with open(filename, "r", encoding="utf8") as reader:
            try:
                self.data = reader.read()
            except:
                self.data = "invalid dropbox entry"
        self.textEditDropbox.setText(self.data)
