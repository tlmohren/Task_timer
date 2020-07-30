from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt

from . import load_config as lc
import pathlib


class Second(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() | Qt.Dialog)

        base_path = pathlib.Path(__file__).parent.parent
        file_config = base_path.joinpath("config.yml")

        self.config_dict = lc.load_config(file_config)

        uic.loadUi(self.config_dict["gui_name"], self)

        screenGeom = QDesktopWidget().availableGeometry()
        sh = screenGeom.height()
        sw = screenGeom.width()
        dx = 325
        dy = 300
        y_offset = 635
        self.setGeometry(sw - dx + 100, sh - dy - y_offset, dx, dy)

        self.setWindowFlag(Qt.FramelessWindowHint)
