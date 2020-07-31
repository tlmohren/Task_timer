from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import json

from . import load_config

import pathlib


class DropboxWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.Dialog)

        base_path = pathlib.Path(__file__).parent.parent
        file_config = base_path.joinpath("config.yml")

        self.config_dict = load_config.load_config(file_config)
        with open(self.config_dict["task_config"], "r") as f:
            self.config = json.load(f)

        uic.loadUi(self.config_dict["gui_name"], self)

        screenGeom = QDesktopWidget().availableGeometry()
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 125
        dy = 100
        if self.config["test_mode"]:
            y_offset = 635
        else:
            y_offset = 235

        self.setWindowTitle("Dropbox todo")
        self.setGeometry(sw - dx + 100, sh - dy - y_offset, dx, dy)

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
