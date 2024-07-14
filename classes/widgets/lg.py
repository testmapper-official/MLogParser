from PyQt6.QtWidgets import QWidget


class LogParser(QWidget):
    def __init__(self, parent=None, directories=None):
        if directories is None:
            directories = []
        super().__init__(parent=parent, strings=directories)
