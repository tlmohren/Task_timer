import pathlib
import sys
from PyQt5 import QtWidgets, QtGui

folder = pathlib.Path(__file__).absolute().parent.parent
sys.path.append(str(folder))

from task_timer import todo_window


def main():

    app = QtWidgets.QApplication([])
    dialog = todo_window.DropboxWindow()
    dialog.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
