#! /usr/bin/env/python
# -*- coding: UTF8 -*-
"""
sqlite_query_data.py
Purpose:
    Provides a widget that enables user to execute queries and view the results
Target System:
    Mac OS X 10.8 and Windows 7
Interface:
    GUI (PyQt)
Functional Requirements:
     Provides a widget that enables user to execute queries and view the results.
    User must provide a valid SQLite3 database connection to this widget
"""

from PyQt4.QtGui import *
from PyQt4.QtSql import *

class QueryDataWidget(QWidget):
    """A widget that provides space to input queries and view results"""

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

        #connections
        self.execute_query_button.clicked.connect(self.query_results)

    def update_connection(self,conn):
        """updates the connection to the current open connection

        Takes one argument:
            conn - the current open database connection
        """

        self.conn = conn

    def query_results(self):
        """executes the query and then displays the results within the widget"""
        
        query = self.query.toPlainText()
        self.conn.query_model(query)
        self.table_view.setModel(self.conn.model)
        self.table_view.show()
        if self.conn.model.lastError().isValid():
            error_dialog = QMessageBox()
            error_dialog.setText(self.conn.model.lastError().databaseText())
            error_dialog.exec()