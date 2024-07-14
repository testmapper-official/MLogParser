import glob
import os
import pickle
from PyQt6.QtCore import Qt, QEvent, QCoreApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTreeWidget, QHeaderView, QHBoxLayout, QFileDialog, QPushButton, QInputDialog, QLineEdit, \
    QTreeWidgetItem
from qframelesswindow.utils.linux_utils import LinuxMoveResize
from classes.widgets import LogParser


class LogTreeChild(QTreeWidgetItem):

    def __init__(self, title):
        super().__init__()

        self.absoluteText = ""
        self.setText(title)

    def setText(self, title, **kwargs):
        self.absoluteText = title
        if 'https://' in title:
            title = title.replace('https://', '').replace('\\', '/').split('/')[0]
        else:
            title = title.replace('\\', '/').split('/')[-1]
        super().setText(0, title)


class LogExplorer(QTreeWidget):
    __BORDER_WIDTH = 5
    __MINIMUM_WIDTH = 175

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__ScaleWidth = self.__MINIMUM_WIDTH
        self.hoverPos = None
        self.isHiddenTree = False
        QCoreApplication.instance().installEventFilter(self)
        self.localViewer = LogTreeChild("Local")
        self.URLViewer = LogTreeChild("URL")

        self.addTopLevelItems([
            self.localViewer,
            self.URLViewer
        ])

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setHeaderLabel("Explorer")

        header = QHeaderView(Qt.Orientation.Horizontal)
        self.openURL = QPushButton(clicked=self.openURL, flat=True)
        self.openURL.setIcon(QIcon("images/open-url.png"))
        self.openURL.setFixedSize(25, 25)
        self.openLocal = QPushButton(clicked=self.openLocal, flat=True)
        self.openLocal.setIcon(QIcon("images/open-folder.png"))
        self.openLocal.setFixedSize(25, 25)
        self.hide = QPushButton("◀", clicked=self.hideTree, flat=True)
        self.hide.setFixedSize(25, 25)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.openURL)
        button_layout.addWidget(self.openLocal)
        button_layout.addWidget(self.hide)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.setContentsMargins(5, 0, 5, 0)
        button_layout.setSpacing(5)
        header.setStyleSheet("""
            QHeaderView {
                background: #232420;
            }       
        """)
        header.setMinimumHeight(35)
        header.setLayout(button_layout)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHeader(header)
        self.expandItem(self.URLViewer)
        self.expandItem(self.localViewer)
        self.fetchCache()

    def hideTree(self):
        self.isHiddenTree = not self.isHiddenTree
        self.openLocal.setVisible(not self.isHiddenTree)
        self.openURL.setVisible(not self.isHiddenTree)
        self.setHeaderLabel("" if self.isHiddenTree else "Explorer")
        self.hide.setText("▶" if self.isHiddenTree else "◀")
        self.adjustWidgets()

    def openURL(self):
        text, ok = QInputDialog().getText(
            None,
            "URL Bitstream",
            "",
            QLineEdit.EchoMode.Normal,
            "https://",
            flags=Qt.WindowType.FramelessWindowHint
        )
        # Input Dialog State
        if not ok:
            return
        # Check on dupes
        # for child in self.URLViewer.takeChildren():
        #     if child.absoluteText == text:
        #         return
        # Server connection
        done = None
        if not done:
            return

        # Add connection to the tree
        child = LogTreeChild(text)
        self.URLViewer.addChild(child)

        self.expandItem(self.URLViewer)

    def createChildTree(self, directory, treeParent):
        child = LogTreeChild(directory)
        treeParent.addChild(child)

        for path in glob.glob(directory + '/*', recursive=False):
            self.createChildTree(path, child)
    def openLocal(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        # Check on dupes
        for index in range(self.localViewer.childCount()):
            if self.localViewer.child(index).absoluteText == directory:
                return

        if directory:
            self.createChildTree(directory, self.localViewer)

        self.expandItem(self.localViewer)


    def fetchCache(self):
        if not os.path.isfile("data/b8_t"):
            return

        with open("data/b8_t", "rb") as cacheFile:
            data = pickle.loads(cacheFile.read())
            if not data:
                return

            for title in data["bURL"]:
                self.URLViewer.addChild(LogTreeChild(title))
            for title in data["bLocal"]:
                self.createChildTree(title, self.localViewer)
            self.__ScaleWidth = data["width"]

    def close(self):
        super().close()

        localArr = []
        for child in self.localViewer.takeChildren():
            localArr.append(child.absoluteText)

        urlArr = []
        for child in self.URLViewer.takeChildren():
            urlArr.append(child.absoluteText)

        data = {
            "bURL": urlArr,
            "bLocal": localArr,
            "width": self.__ScaleWidth,
        }

        bitstream = bytearray(pickle.dumps(data))

        with open("data/b8_t", "wb") as cacheFile:
            cacheFile.write(bitstream)

    def getScaledWidth(self):
        if self.isHiddenTree:
            return 40

        return self.__ScaleWidth

    def adjustWidgets(self):

        if not self.parent():
            raise Exception("No parent found")

        self.parent().adjustWidgets()

    def setScaleWidth(self, val):
        self.__ScaleWidth = val

        if self.__ScaleWidth < self.__MINIMUM_WIDTH:
            self.__ScaleWidth = self.__MINIMUM_WIDTH
        elif self.__ScaleWidth > self.parent().width() * 0.95:
            self.__ScaleWidth = int(self.parent().width() * 0.95)

        self.adjustWidgets()

    def itemDoubleClicked(self, item, column):
        print(item.absoluteText)

        if not os.path(item.absoluteText).isfile():
            super().itemDoubleClicked(item, column)
            return

        self.parent().createTab(item.absoluteText)


    def eventFilter(self, obj, event):
        et = event.type()
        if et == QEvent.Type.MouseButtonRelease:
            self.hoverPos = None
        elif et != QEvent.Type.MouseButtonPress and et != QEvent.Type.MouseMove:
            return False

        edges = Qt.Edge(0)
        posAbs = event.globalPosition().toPoint()
        pos = posAbs - self.parent().pos()
        print(posAbs.x(), self.hoverPos.x() if self.hoverPos else None, pos.x(), self.getScaledWidth() - self.__BORDER_WIDTH)
        if pos.x() >= self.getScaledWidth() - self.__BORDER_WIDTH:
            edges |= Qt.Edge.RightEdge

        # change cursor
        if et == QEvent.Type.MouseButtonPress and self.windowState() == Qt.WindowState.WindowNoState:
            if edges in Qt.Edge.RightEdge:
                self.hoverPos = pos
        if et == QEvent.Type.MouseMove and self.windowState() == Qt.WindowState.WindowNoState:
            if self.hoverPos and edges in Qt.Edge.RightEdge:
                oldWidth = self.getScaledWidth()
                self.setScaleWidth(self.__ScaleWidth + pos.x() - self.hoverPos.x())
                if oldWidth != self.getScaledWidth():
                    self.hoverPos = pos
            if edges in Qt.Edge.RightEdge:
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        return super().eventFilter(obj, event)
