#! /usr/bin/env/python
# -*- coding: UTF8 -*-
"""
sqlite_entity_descriptions.py
Purpose:
    Provides a widget that displays entity descriptions from a SQLite3 database
Target System:
    Mac OS X 10.8 and Windows 7
Interface:
    GUI (PyQt)
Functional Requirements:
     Provides a widget that displays entity descriptions from a SQLite3 databases.
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
from PyQt4.QtCore import *

class EntityDescriptionWidget(QWidget):
    """A widget that can display entity descriptions from an open database connection"""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.entity_description = QTextEdit()
        self.entity_description.setReadOnly(True)
        self.entity_description.setMinimumWidth(500)

        self.layout.addWidget(self.entity_description)
        self.setLayout(self.layout)

    def update_layout(self,conn):
        """updates the widget to contain entity descriptions from the current open database connection

        Takes one argument:
            conn - the current open database connection
        """

        conn.relational_table_model()
        descriptions = ""
        for each in range(len(conn.db.tables())):
            descriptions += self.create_entity_description(each,conn)
            descriptions += "<br/>"
        self.entity_description.setHtml(descriptions)

    def create_entity_description(self,index,conn):
        """creates a HTML text string containing the entity description for the provided entity

        Takes two arguments:
            index - the index value for the entity
            conn - the current open database connection

        Return values:
            entity_desc - the HTML text for the entity description
        """

        entity_desc = ""
        conn.model.setTable(conn.db.tables()[index])
        conn.model.select()

        #get the column names
        attributes = []
        for each in range(conn.model.columnCount()):
            attributes.append(conn.model.headerData(each,Qt.Horizontal))

        #check for primary keys
        primary_key = conn.model.primaryKey()
        primary_attributes = primary_key.count()
        for each in range(primary_attributes):
            search_value = primary_key.field(each).name()
            if search_value in attributes:
                i = attributes.index(search_value)
                attributes[i] = "<u>{0}</u>".format(attributes[i])

        #check for foreign keys
        sql = ("pragma foreign_key_list({0})".format(conn.db.tables()[index]))
        conn.run_query(sql)
        result = conn.query_result.first()
        if result:
            more_keys = True
            while more_keys:
                search_value = conn.query_result.value(4)
                if search_value in attributes:
                    i = attributes.index(search_value)
                    attributes[i] = "<i>{0}</i>".format(attributes[i])
                more_keys = conn.query_result.next()


        #create entity description
        entity_desc += "<b>{0}</b>(".format(conn.db.tables()[index])
        entity_desc += attributes[0]
        for each in attributes[1:]:
            entity_desc += ",{0}".format(each)            
        entity_desc += ")"
        return entity_desc
