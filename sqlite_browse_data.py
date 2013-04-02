from PyQt4.QtGui import *
from PyQt4.QtSql import *

class BrowseDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.available_tables = QComboBox()
        self.table_view = QTableView()

        self.conn = None

        self.layout.addWidget(self.available_tables)
        self.layout.addWidget(self.table_view)

        self.setLayout(self.layout)

        #connections
        self.available_tables.currentIndexChanged.connect(self.change_table)

    def update_layout(self,conn):
        self.available_tables.clear()
        self.conn = conn
        self.available_tables.addItems(conn.db.tables())
        conn.relational_table_model()
        self.change_table(0)
        #else:
            #conn.model.select() #refresh the view

        

    def change_table(self,index):
        try:
            self.conn.model.setTable(self.conn.db.tables()[index])
            self.conn.model.select()
            self.table_view.setModel(self.conn.model)
        except AttributeError:
            pass
        #conn.table_view.show()


