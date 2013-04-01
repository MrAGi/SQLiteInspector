import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from sqlite_entity_descriptions import *
from sqlite_browse_data import *
from sqlite_query_data import *

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.load_database = self.file_menu.addAction("Load Database")

        self.tab_bar = QTabWidget()

        self.tab_desc = EntityDescriptionWidget()
        self.tab_data = BrowseDataWidget()
        self.tab_query = QueryDataWidget()
        
        self.db = None
        self.file = None

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
        self.file = QFileDialog.getOpenFileName(caption="Open Database",filter="Database file (*.db *.dat)")
        if len(self.file) > 0:
            if self.db:
                self.tab_desc.model = None
                self.db.database().close()
                self.db.removeDatabase(self.db.connectionName())
            self.open_database_connection(self.file)
            #QSqlQuery("PRAGMA foreign_keys = ON")
            self.set_up_tab(self.tab_bar.currentIndex())

    def open_database_connection(self,file):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(file)
        ok = self.db.open()

    def set_up_tab(self,tab):
        if tab == 0:
            self.tab_desc.update_layout(self.db)
        elif tab == 1:
            self.tab_data.update_layout(self.db)
        elif tab == 2:
            self.tab_query.update_db(self.db)


def main():
    application = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()

if __name__ == '__main__':
    main()