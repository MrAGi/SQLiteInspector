#Read Me
Last Updated - 4th April 2013.

##The Program
SQLite Inspector provides a method of browsing data, executing queries and viewing the entity descriptions of a valid SQLite3 database file.

It has been developed to assist A-Level students who are developing projects using a combination of Python 3, SQLite 3 and PyQt 4. SQLite Inspector provides a way for them to ensure:

- that any changes they have made to the database have been successful
- to test the syntax of their queries
- to check their entity descriptions

This project takes its main inspiration from [SQLite Database Browser][1], which we had been using previously for this task. Unfortunately, there are bugs in that program that mean that it was frustrating for my students to use. Since the project does not appear to be actively maintained and as I am not a C programmer, I decided to write a similar utility in Python that would have only the features that we need. 

##Known Issues
The program has not been extensively tested yet and therefore may not function as intended. Therefore, if you are working with critical data you should back it up before using it with this program.

Known issues include:

- When switching back to the "Browse data" tab the first table is always shown even if you had previously displayed another table (Fixed 05/04/2013)

##Licensing

This is my first attempt at an open source project and therefore I am unsure that I have correctly licensed all of the code. My intention is that all of the code is available under the [GPL version 3][2] license. 

Please let me know if I have messed this up!

##Finally

I have mainly created this program to help my own students with their A-Level projects but I hope that it is useful for other teachers and maybe others as well. 

I am happy to receive feedback and if you would like to contribute you can find the main repository for this project on my [github][3] page.

Thanks,

Adam. (adam@mcnicol.me)

[1]: http://sqlitebrowser.sourceforge.net
[2]: http://opensource.org/licenses/GPL-3.0
[3]: https://github.com/MrAGi/SQLiteInspector