from qframelesswindow import StandardTitleBar


class TitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.__TITLE_HEIGHT = 20
        # customize the style of title bar button
        self.closeBtn.setStyleSheet("""
                        TitleBarButton {
                            qproperty-normalColor: white;
                        }
        """)
        self.minBtn.setStyleSheet("""
                        TitleBarButton {
                            qproperty-normalColor: white;
                            qproperty-hoverColor: white;
                            qproperty-hoverBackgroundColor: #4e5754;
                            qproperty-pressedColor: white;
                            qproperty-pressedBackgroundColor: #65706c;
                        }
                    """)
        self.maxBtn.setStyleSheet("""
                TitleBarButton {
                    qproperty-normalColor: white;
                    qproperty-hoverColor: white;
                    qproperty-hoverBackgroundColor: #4e5754;
                    qproperty-pressedColor: white;
                    qproperty-pressedBackgroundColor: #65706c;
                }
            """)

        self.titleLabel.setStyleSheet("""
            QLabel {
                fontcolor: white;
                font: 13px 'Segoe UI';
                padding: 0 4px
            }
        """)
