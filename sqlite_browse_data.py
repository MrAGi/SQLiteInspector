from PyQt4.QtGui import *
from PyQt4.QtSql import *

class BrowseDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.available_tables = QComboBox()
        self.table_view = QTableView()

        self.db = None
        self.model = None

        self.layout.addWidget(self.available_tables)
        self.layout.addWidget(self.table_view)

        self.setLayout(self.layout)

        #connections
        self.available_tables.currentIndexChanged.connect(self.change_table)

    def update_layout(self,db):
        if db != None and self.db == None:
            self.db = db
            self.available_tables.clear()
            self.available_tables.addItems(self.db.tables())
            self.model = QSqlRelationalTableModel()
            self.change_table(0)
        else:
            self.model.select() #refresh the view

        

    def change_table(self,index):
        if self.model != None:
            self.model.setTable(self.db.tables()[index])
            self.model.select()
            self.table_view.setModel(self.model)
            self.table_view.show()


