import pymysql
import pandas as pd

DB_LEN = 5                  # Global DB_LEN is mainly used in function add_project


def establish_project():
    """
       Main fucntion will establish the connection with MySQL,
       create an initial table, and call main menu.
       @return: None
       """

    # Establish database connection with root and passport
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()

    # If table exist, then drop it to establish a new one.
    cursor.execute("DROP TABLE IF EXISTS PROJECT")

    # Esatabilsh an initually table consisted of project name, 5 names and number of members.
    # If users enter more than 5 names, we will extend more columns to store name in add_project function.
    sql = """CREATE TABLE PROJECT (
                    PROJECT_NAME CHAR(20),
                    NAME1  CHAR(20) NOT NULL,
                    NAME2  CHAR(20) ,
                    NAME3  CHAR(20) ,
                    NAME4  CHAR(20) ,
                    NAME5  CHAR(20) ,
                    NUMBER INT )"""

    cursor.execute(sql)
    db.close()


def DB_show():
    """
        After connection with MySQL, this function get all the
        values stored in the table PROJECT. Fetch them, transform
        them into DataFrame, print them to users. DataFrame could
        be used for data analysis and calculation later.
        @return:
        """
    # Connect again
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql_show = "select * from PROJECT"
    try:

        cursor.execute(sql_show)
        result = cursor.fetchall()  # fetch function return TUPLE
    finally:
        db.close()
    df = pd.DataFrame(list(result))  # Convert tuple to list, then DataFrame
    print(df)


def add_project(project_name, number, name_list):
    """
    This function could create or add a project into the database,
    which will generate a data row in the table PROJECT.

    Global variable DB_LEN is used to record how many columns is used
    to store member names in table.In main function, we initialize the
    table with 5 names. If users enter more than 5 names, we have to
    extend the storage space.


    @type project_name: string
    @param project_name: Project name
    @type number: int
    @param number: Count of members.
    @type name_list: list
    @param name_list:
    @return: None
    """

    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    multi_name = ''                 # Create a string to store member name.
    sql_values = """'%s',""" % project_name

    global DB_LEN
    if number > DB_LEN:
        # Users enter more names than the maximum of former input, extend columns.
        for count_add in range(DB_LEN+1, len(name_list)+1, 1):
            # Create a string to alter table.
            add_value = 'NAME%d' % count_add
            sql_add_obeject = '''alter table PROJECT add %s CHAR(20) after NAME%d
            ''' % (add_value, count_add-1)
            try:
                # submit to databse to run
                cursor.execute(sql_add_obeject)
                db.commit()
            except ValueError as e:
                # if error happens, rollback
                print('database execution error!')
                db.rollback()
            DB_LEN = number             # Renew the DB_LEN

    # Create a string to add data into database
    for count1 in range(number):
        multi_name += 'NAME%d, ' % (count1+1)

    for count2 in name_list:
        sql_values += """'%s', """ % count2

    sql = """INSERT INTO PROJECT(PROJECT_NAME,
             %s NUMBER)
             VALUES (%s %d)""" % (multi_name, sql_values, number)
    try:
        cursor.execute(sql)
        db.commit()
    except ValueError as e:
        print('database execution error!')
        db.rollback()
    db.close()

