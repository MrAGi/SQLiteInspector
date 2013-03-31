from PyQt4.QtGui import *
from PyQt4.QtSql import *

class QueryDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.query = QTextEdit()
        self.execute_query_button = QPushButton("Execute Query")
        self.table_view = QTableView()

        self.layout.addWidget(self.query)
        self.layout.addWidget(self.execute_query_button)
        self.layout.addWidget(self.table_view)

        self.setLayout(self.layout)
        self.db = None

        #connections
        self.execute_query_button.clicked.connect(self.query_results)

    def update_db(self,db):
        self.db = db

    def query_results(self):
        query = self.query.toPlainText()
        self.model = QSqlQueryModel()
        self.model.setQuery(query)
        self.table_view.setModel(self.model)
        self.table_view.show()
        if self.model.lastError().isValid():
            error_dialog = QMessageBox()
            error_dialog.setText(self.model.lastError().databaseText())
            error_dialog.exec()