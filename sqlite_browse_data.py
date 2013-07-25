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
Licence:
    Copyright (C) 2013  Adam McNicol

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
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
        self.current_table = None

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
        self.conn = conn
        self.conn.relational_table_model()
        #gets text for each item in the available_tables combobox and puts it in a list
        current_items = [self.available_tables.itemText(i) for i in range(self.available_tables.count())]
        if not (current_items == conn.db.tables()) or not(isinstance(conn.model,QSqlRelationalTableModel)):
            self.available_tables.clear()
            #self.conn = conn
            #self.conn.relational_table_model()
            self.available_tables.addItems(conn.db.tables())
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
            self.current_table = index
        except AttributeError as e:
            print(e)
        #conn.table_view.show()

    def refresh(self):
        try:
            self.conn.model.setTable(self.conn.db.tables()[self.current_table])
            self.conn.model.select()
            self.table_view.setModel(self.conn.model)
            #self.conn.model.select()
        except AttributeError as e:
            print(e)


