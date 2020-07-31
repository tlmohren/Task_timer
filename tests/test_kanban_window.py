import pathlib
import sys
from PyQt5 import QtWidgets, QtGui

folder = pathlib.Path(__file__).absolute().parent.parent
sys.path.append(str(folder))

from task_timer import kanban_window


def main():

    app = QtWidgets.QApplication([])
    dialog = kanban_window.KanbanWindow()
    dialog.show()

    dialog.update_kanban()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
