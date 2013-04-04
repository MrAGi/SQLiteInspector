#! /usr/bin/env/python
# -*- coding: UTF8 -*-
"""
sqlite_browser.py
Purpose:
    View tables, check queries and see entity descriptions for a SQLite3 database
Target System:
    Mac OS X 10.8 and Windows 7
Interface:
    GUI (PyQt)
Functional Requirements:
    Provides an interface to browse tables, execute queries and view enity descriptions.
    User must provide a valid SQLite3 database with extension of *.db or *.dat
"""

__version__ = 0.1
__status__ = "Prototype"
__date__ = "04-04-2013"
__maintainer__ = "adam@mcnicol.me"
__credits__ = "Inspired by SQLite Database Browser"

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from sqlite_entity_descriptions import *
from sqlite_browse_data import *
from sqlite_query_data import *
from sqlite_connection import *

class BrowserWindow(QMainWindow):
    """Creates the main window for the application"""
    def __init__(self):
        super().__init__()

        self.db_connection = None

        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.load_database = self.file_menu.addAction("Load Database")

        self.tab_bar = QTabWidget()

        self.tab_desc = EntityDescriptionWidget()
        self.tab_data = BrowseDataWidget()
        self.tab_query = QueryDataWidget()

        self.tab_bar.addTab(self.tab_desc,"Entity Descriptions")
        self.tab_bar.addTab(self.tab_data,"Browse Data")
        self.tab_bar.addTab(self.tab_query,"Execute Query")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_bar)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        #connections
        self.load_database.triggered.connect(self.load_database_file)
        self.tab_bar.currentChanged.connect(self.set_up_tab)

    def load_database_file(self):
        """asks the user for the database file to load and ensures any previous database
            connections are closed before opening a new connection to the given file
        """
        #ensure that model is removed so that connection to database can be closed
        self.tab_data.table_view.setModel(None)
        self.tab_query.table_view.setModel(None)

        path = QFileDialog.getOpenFileName(caption="Open Database",filter="Database file (*.db *.dat)")
        if len(path) > 0:
            #already have a connection object
            if self.db_connection:
                self.db_connection.path = path
            else:
                self.db_connection = SQLConnection(path)
            
            self.db_connection.open_database()
            self.set_up_tab(self.tab_bar.currentIndex())

    def set_up_tab(self,tab):
        if tab == 0:
            self.tab_desc.update_layout(self.db_connection)
        elif tab == 1:
            self.tab_data.update_layout(self.db_connection)
        elif tab == 2:
            self.tab_query.update_connection(self.db_connection)


def main():
    application = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()

if __name__ == '__main__':
    main()