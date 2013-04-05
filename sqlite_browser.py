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

        #add about option to menu 
        if sys.platform != "darwin":
            self.help_menu = self.menu_bar.addMenu("Help")
            self.about = self.help_menu.addAction("abouttest")
        else:
            self.about = self.file_menu.addAction("abouttest")

        self.load_database = self.file_menu.addAction("Load Database")
        self.load_database_icon = QIcon(QPixmap("open.png"))
        self.load_database.setIcon(self.load_database_icon)
        self.load_database.setShortcut(QKeySequence("Ctrl+o"))

        self.refresh_database = self.file_menu.addAction("Refresh Database")
        self.refresh_database.setDisabled(True)
        self.refresh_database_icon = QIcon(QPixmap("refresh.png"))
        self.refresh_database.setIcon(self.refresh_database_icon)
        self.refresh_database.setShortcut(QKeySequence("F5"))

        self.tab_bar = QTabWidget()

        self.tab_desc = EntityDescriptionWidget()
        self.tab_data = BrowseDataWidget()
        self.tab_query = QueryDataWidget()

        self.tab_bar.addTab(self.tab_desc,"Entity Descriptions")
        self.tab_bar.addTab(self.tab_data,"Browse Data")
        self.tab_bar.addTab(self.tab_query,"Execute Query")

        self.tool_bar = QToolBar("Manage Databases")
        self.tool_bar.setMovable(False)
        self.tool_bar.setIconSize(QSize(20,20))

        self.tool_bar.addAction(self.load_database)
        self.tool_bar.addAction(self.refresh_database)

        self.addToolBar(self.tool_bar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_bar)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setMenuWidget(self.menu_bar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle("SQLite Inspector")

        #connections
        self.load_database.triggered.connect(self.load_database_file)
        self.about.triggered.connect(self.about_application)
        self.tab_bar.currentChanged.connect(self.set_up_tab)
        self.refresh_database.triggered.connect(self.refresh)

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
            
            ok = self.db_connection.open_database()
            self.set_up_tab(self.tab_bar.currentIndex())

    def set_up_tab(self,tab):
        """updates the current tab by providing the current database connection to the update method of the
        appropriate main_widget

        Takes one argument:
            tab - the index value for selected tab
        """
        if self.db_connection:
            if tab == 0:
                self.refresh_database.setDisabled(True)
                self.tab_desc.update_layout(self.db_connection)
            elif tab == 1:
                self.refresh_database.setDisabled(False)
                self.tab_data.update_layout(self.db_connection)
            elif tab == 2:
                self.refresh_database.setDisabled(True)
                self.tab_query.update_connection(self.db_connection)

    def about_application(self):
        dialog = QDialog()
        dialog.setWindowTitle("About SQLite Inspector")
        dialog.exec_()

    def refresh(self):
        if self.tab_bar.currentIndex() == 1:
            self.tab_data.refresh()


def main():
    application = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()

if __name__ == '__main__':
    main()