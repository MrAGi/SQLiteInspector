from PyQt4.QtGui import *

class QueryDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.test_label = QLabel("query data")
        self.layout.addWidget(self.test_label)
        self.setLayout(self.layout)
        self.file = ""