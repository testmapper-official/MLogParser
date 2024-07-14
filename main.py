import sys
import classes.errorhandler
from classes import MainWindow, excepthook
from PyQt6.QtWidgets import QApplication

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = MainWindow()
    demo.show()
    sys.exit(app.exec())
