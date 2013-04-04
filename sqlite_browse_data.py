#! /usr/bin/env/python
# -*- coding: UTF8 -*-
"""
sqlite_browse_data.py
Purpose:
    Provides a widget that enables user to view entity data and switch between available entities
Target System:
    Mac OS X 10.8 and Windows 7
Interface:
    GUI (PyQt)
Functional Requirements:
     Provides a widget that enables user to view entity data and switch between available entities.
    User must provide a valid SQLite3 database connection to this widget
"""

from PyQt4.QtGui import *
from PyQt4.QtSql import *

class BrowseDataWidget(QWidget):
    """A widget that can display entity data and switch between available entities"""
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
        """updates the widget to contain entities from the current open database connection

        Takes one argument:
            conn - the current open database connection
        """

        self.available_tables.clear()
        self.conn = conn
        self.available_tables.addItems(conn.db.tables())
        conn.relational_table_model()
        self.change_table(0)

    def change_table(self,index):
        """updates the widget to contain entity data from the selected entity

        Takes one argument:
            index - the index value of the required entity
        """

        try:
            self.conn.model.setTable(self.conn.db.tables()[index])
            self.conn.model.select()
            self.table_view.setModel(self.conn.model)
        except AttributeError:
            pass
        #conn.table_view.show()


