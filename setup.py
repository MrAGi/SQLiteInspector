# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

application_title = "SQLite Inspector" #what you want to application to be called
main_python_file = "sqlite_browser.py" #the name of the python file you use to run the program
application_version = "0.1"
application_description = "SQLite Inspector alls you to view data, execute queries and see entity descriptions"
windows_icon = "sqlinspector.ico"
mac_icon = "sqlinspector.icns"

import sys
import os

from cx_Freeze import setup, Executable

base = None

includes = ["atexit","re"]

if sys.platform == "win32":
    base = "Win32GUI"
    include_files = [("C:\Python32\Lib\site-packages\PyQt4\plugins\sqldrivers","sqldrivers")]
    build_options = {"path": sys.path,
                 "includes": includes,
                 "include_files":include_files,
                 "icon":windows_icon
                }
else:
    include_files = [("/opt/local/share/qt4/plugins/sqldrivers","sqldrivers")]
    build_options = {"path": sys.path,
                 "includes": includes,
                 "include_files":include_files
                }

if sys.platform == "win32":
    setup(
            name = application_title,
            version = application_version,
            description = application_description,
            options = {"build_exe" : build_options},
            executables = [Executable(main_python_file, base = base)])
else:
    setup(
            name = application_title,
            version = application_version,
            description = application_description,
            options = {"build_exe" : build_options},
            executables = [Executable(main_python_file, base = base, targetName= application_title)])

