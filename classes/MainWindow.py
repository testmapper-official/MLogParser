from qframelesswindow import FramelessWindow
from classes.widgets import LogParser, TitleBar, TabLogger, LogExplorer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QLabel


class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.setTitleBar(TitleBar(self))

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        # self.label.setPixmap(QPixmap(""))

        self.setMinimumWidth(200)
        self.setMinimumHeight(200)

        self.setWindowIcon(QIcon("screenshot/logo.png"))
        self.setWindowTitle("Mi Log Parser v0.1")

        self.titleBar.raise_()
        self.tab = TabLogger(self)
        self.tree = LogExplorer(self)

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)

        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(
            self.width() // 2 - length // 2,
            self.height() // 2 - length // 2
        )

        self.adjustWidgets()

    def adjustWidgets(self):
        tree_width = self.tree.getScaledWidth()
        tab_width = self.width() - tree_width

        if tab_width / self.width() < 0.05:
            tab_width = int(0.05 * self.width())
            tree_width = self.width() - tab_width

        self.tree.setGeometry(0, self.titleBar.height(), tree_width, self.height() - self.titleBar.height())
        self.tab.setGeometry(tree_width, self.titleBar.height(), tab_width,
                             self.height() - self.titleBar.height())

    def createTab(self, directory):
        print(directory)

    def close(self):
        self.tree.close()
        self.tab.close()

        super().close()
