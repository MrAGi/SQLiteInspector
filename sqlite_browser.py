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

    def load_database_file(self):
        self.file = QFileDialog.getOpenFileName(caption="Open Database",filter="Database file (*.db *.dat)")
        self.tab_desc.file = self.file
        self.tab_data.file = self.file
        self.tab_query.file = self.file


def main():
    application = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()

if __name__ == '__main__':
    main()