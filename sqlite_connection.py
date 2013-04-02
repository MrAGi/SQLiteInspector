from PyQt4.QtSql import *
from PyQt4.QtGui import *

class SQLConnection:
    def __init__(self,path):
        super().__init__()
        self.path = path
        self.db = None
        self.model = None
        self.query_result = None

    def open_database(self):
        if self.db:
            self.close_database()

        self.db = QSqlDatabase.addDatabase("QSQLITE", "conn")

        self.db.setDatabaseName(self.path)
        self.db.open()

    def close_database(self):
        if self.view:
            self.view.setModel(None)
        del self.model
        del self.query_result
        self.db.close()
        del self.db
        QSqlDatabase.removeDatabase("conn")

    def closeEvent(self, event):
        self.close_database()

    def table_model(self):
        if not self.db.isOpen():
            self.open_database()

       # if self.model:
          #  del self.model

        self.model = QSqlTableModel(db=self.db)
        self.model.setTable(self.db.tables()[0])
        self.model.select()

    def relational_table_model(self):
        if not self.db.isOpen():
            self.open_database()

       # if self.model:
         #   del self.model

        self.model = QSqlTableModel(db=self.db)
        self.model.setTable(self.db.tables()[0])
        self.model.select()

    def query_model(self,sql):
        if not self.db.isOpen():
            self.open_database()

        #if self.model:
          #  del self.model

        self.model = QSqlQueryModel()
        self.model.setQuery(sql,db=self.db)

    def run_query(self,sql):
        if not self.db.isOpen():
            self.open_database()

        self.query_result = QSqlQuery(sql,db=self.db)

