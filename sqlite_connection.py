#! /usr/bin/env/python
# -*- coding: UTF8 -*-
"""
sqlite_connection.py
Purpose:
    Provides a class that can be instantiated to manage connections to a SQLite3 database
Target System:
    Mac OS X 10.8 and Windows 7
Interface:
    GUI (PyQt)
Functional Requirements:
     Provides a class that can be instantiated to manage connections to a SQLite3 databases.
    User must provide a valid path to a SQLite3 database
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
        """opens the datbase on the current path and closes any previously opened connections"""

        if self.db:
            self.close_database()

        self.db = QSqlDatabase.addDatabase("QSQLITE", "conn")

        self.db.setDatabaseName(self.path)
        ok = self.db.open()
        return ok

    def close_database(self):
        """closes the datbase that is currently open"""
        del self.model
        del self.query_result
        self.db.close()
        del self.db
        QSqlDatabase.removeDatabase("conn")

    def closeEvent(self, event):
        self.close_database()

    def table_model(self):
        """sets the model for the current connection to a QSqlTableModel and sets the current table to
        the first table in the database
        """

        if not self.db.isOpen():
            self.open_database()

        self.model = QSqlTableModel(db=self.db)
        self.model.setTable(self.db.tables()[0])
        self.model.select()

    def relational_table_model(self):
        """sets the model for the current connection to a QSqlRelationalTableModel and sets the current table to
        the first table in the database
        """

        if not self.db.isOpen():
            self.open_database()

        self.model = QSqlRelationalTableModel(db=self.db)
        self.model.setTable(self.db.tables()[0])
        self.model.select()

    def query_model(self,sql):
        """sets the model for the current connection to a QSqlQueryModel executes the given query

        Takes one argument:
            sql - the sql query to be executed
        """

        if not self.db.isOpen():
            self.open_database()

        self.model = QSqlQueryModel()
        self.model.setQuery(sql,db=self.db)

    def run_query(self,sql):
        """executes a given query on the current connection

        Takes one argument:
            sql - the sql query to be executed
        """

        if not self.db.isOpen():
            self.open_database()

        self.query_result = QSqlQuery(sql,db=self.db)

