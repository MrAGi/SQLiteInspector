from PyQt4.QtGui import *

class EntityDescriptionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.test_label = QLabel("test")
        self.layout.addWidget(self.test_label)
        self.setLayout(self.layout)
        self.file = ""