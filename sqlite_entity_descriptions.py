from PyQt4.QtGui import *

class EntityDescriptionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.test_label = QLabel("test")
        self.layout.addWidget(self.test_label)
        self.setLayout(self.layout)
        self.db = None

    def update_layout(self,db):
        if self.db:
            if self.db != db:
                self.db = db
                self.available_tables.clear()
                self.available_tables.addItems(self.db.tables())
        else:
            self.db = db
            self.available_tables.clear()
            self.available_tables.addItems(self.db.tables())
        self.model = QSqlTableModel()