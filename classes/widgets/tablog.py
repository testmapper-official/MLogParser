from PyQt6.QtWidgets import QTabWidget


class TabLogger(QTabWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setTabsClosable(True)
        self.setAutoFillBackground(True)
        self.tabCloseRequested.connect(self.onTabClose)

    def onTabClose(self, index):
        self.removeTab(index)
