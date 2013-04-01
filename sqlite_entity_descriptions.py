from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4.QtCore import *

class EntityDescriptionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.entity_description = QTextEdit()

        self.layout.addWidget(self.entity_description)
        self.setLayout(self.layout)

        self.db = None
        self.model = None

    def update_layout(self,db):
        if db != None:
            self.db = db
            self.model = QSqlRelationalTableModel()
            descriptions = ""
            for each in range(len(self.db.tables())):
                descriptions += self.create_entity_description(each)
                descriptions += "<br/>"
            self.entity_description.setHtml(descriptions)

    def create_entity_description(self,index):
        if self.model != None:
            entity_desc = ""
            self.model.setTable(self.db.tables()[index])
            self.model.select()

            #get the column names
            attributes = []
            for each in range(self.model.columnCount()):
                attributes.append(self.model.headerData(each,Qt.Horizontal))

            #check for primary keys
            primary_key = self.model.primaryKey()
            primary_attributes = primary_key.count()
            for each in range(primary_attributes):
                search_value = primary_key.field(each).name()
                if search_value in attributes:
                    i = attributes.index(search_value)
                    attributes[i] = "<u>{0}</u>".format(attributes[i])

            #check for foreign keys
            sql = ("pragma foreign_key_list({0})".format(self.db.tables()[index]))
            query = QSqlQuery(sql)
            result = query.first()
            if result:
                more_keys = True
                while more_keys:
                    search_value = query.value(4)
                    if search_value in attributes:
                        i = attributes.index(search_value)
                        attributes[i] = "<i>{0}</i>".format(attributes[i])
                    more_keys = query.next()


            #create entity description
            entity_desc += "<b>{0}</b>(".format(self.db.tables()[index])
            entity_desc += attributes[0]
            for each in attributes[1:]:
                entity_desc += ",{0}".format(each)            
            entity_desc += ")"
            return entity_desc
