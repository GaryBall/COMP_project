import pymysql
import pandas as pd


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
                    MEMBER_NUMBER INT ,
                    NAME1  CHAR(20) NOT NULL,
                    NAME2  CHAR(20) NOT NULL,
                    NAME3  CHAR(20) ,
                    NAME4  CHAR(20) ,
                    NAME5  CHAR(20) )"""

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
        print('you have following projects:')
        for row in result:
            print(row[0])
    except ValueError as e:
        print("database show failed")

    selection = input("Choose a project to see the member.")

    sql_show = "select * from %s" % selection

    try:
        cursor.execute(sql_show)
        result = cursor.fetchall()
        for row in result:
            print(row)
    finally:
        db.close()


DB_LEN = 5                  # Global DB_LEN is mainly used in function add_project


def DB_show_project():
    """
    This function show the projects in the database. Compare to DB_show,
    it can not show the detailed content of specific project
    @return:
    """
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql_show = "select * from PROJECT"
    try:

        cursor.execute(sql_show)
        result = cursor.fetchall()  # fetch function return TUPLE
        print('you have following projects:')
        for row in result:
            print(row[0])
    except ValueError as e:
        print("database show failed")

    db.close()


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
    multi_name = ''  # Create a string to store member name.
    sql_values = """'%s',""" % project_name

    global DB_LEN
    print(number, type(number))
    print(type(DB_LEN))
    if number > DB_LEN:
        # Users enter more names than the maximum of former input, extend columns.
        for count_add in range(DB_LEN + 1, len(name_list) + 1, 1):
            # Create a string to alter table.
            add_value = 'NAME%d' % count_add
            sql_add_obeject = '''alter table PROJECT add %s CHAR(20) after NAME%d
                    ''' % (add_value, count_add - 1)
            try:
                # submit to databse to run
                cursor.execute(sql_add_obeject)
                db.commit()
            except ValueError as e:
                # if error happens, rollback
                print('database execution error!')
                db.rollback()
            DB_LEN = number  # Renew the DB_LEN

    # Create a string to add data into database
    for count1 in range(number):
        multi_name += 'NAME%d, ' % (count1 + 1)

    for count2 in name_list:
        sql_values += """'%s', """ % count2

    sql = """INSERT INTO PROJECT(PROJECT_NAME,
                     %s MEMBER_NUMBER)
                     VALUES (%s %d)""" % (multi_name, sql_values, number)
    try:
        cursor.execute(sql)
        db.commit()
    except ValueError as e:
        print('database execution error!')
        db.rollback()

        '''
        UPDATE PROJECT SET MEMBER_NUM = 7 WHERE PROJECT_NAME = 'pA'
        '''


def create_person_table(project_name, member_list):
    """
    Create a tables in database to store the vote data from members.
    This table contains project name, member name and name list of members.

    @type project_name: string
    @param project_name:
    @type member_list: list
    @param member_list:
    @return:
    """
    sql_member_list = ''
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS %s" % project_name)

    for member in member_list:
        sql_member_list += ''',\n\t%s INT''' % member

    sql = '''CREATE TABLE %s (
    PERSON_NAME CHAR(20)%s) 
    '''% (project_name, sql_member_list)
    print(sql)
    cursor.execute(sql)
    db.commit()
    db.close()


def get_member_num(project_name):
    """
    This function get the member numbers of a project from table PROJECT
    @type string
    @param project_name:
    @return:
    """
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()

    sql  = """select * from PROJECT
              where PROJECT_NAME = '%s'
    """ % project_name

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            name = row[1]
    except ValueError as e:
        print('No results!')
        db.rollback()
    db.close()

    return name


def add_member_num(project_name, member_number):
    """

    @param project_name:
    @param member_number:
    @return:
    """
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()

    sql = """
    UPDATE PROJECT 
    SET MEMBER_NUMBER= %d WHERE PROJECT_NAME='%s';
        """ % member_number, project_name

    try:
        cursor.execute(sql)
        db.commit()
    except ValueError as e:
        print('Adding failed')
        db.rollback()
    db.close()


def get_name_list(project_name):
    """
    get name list from table PROJECT of database by input project name.


    @type project_name: string
    @param project_name:
    @return:
    """
    member_list = []
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql = """select * from PROJECT
              where PROJECT_NAME = '%s'
              """ % project_name

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for i in range(2, len(row)):
                if row[i] is not None:
                    member_list.append(row[i])
    except ValueError as e:
        print('Fetch failed')
        db.rollback()

    db.close()
    return member_list


def add_vote_list(project_name, member_name, name_list, the_vote_list):
    """
    Store vote list of a specific member into database. This vote list
    is the mark a member vote to others.

    @type project_name: string
    @param project_name:
    @type member_name: string
    @param member_name:
    @type name_list: list
    @param name_list:
    @type the_vote_list: list
    @param the_vote_list:
    @return:
    """

    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql_name_list = ''
    sql_vote_list = ''
    for vote in the_vote_list:
        sql_vote_list += ''', %s''' % vote
    for name in name_list:
        sql_name_list += ',%s' % name

    sql = """INSERT INTO %s(PERSON_NAME%s)
            VALUES ('%s' %s)""" % (project_name, sql_name_list, member_name, sql_vote_list)

    print(sql)
    cursor.execute(sql)
    db.commit()

    db.close()


def get_vote_list(table_name, person_name):
    """
    This function can get the vote list from the table of input project
    according to the table_name and person_name

    @param table_name:
    @param person_name:
    @return:
    """
    member_vote = []
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql = """select * from %s
                  where PERSON_NAME = '%s'
                  """ % (table_name, person_name)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for i in range(1, len(row)):
                if row[i] is not None:
                    member_vote.append(row[i])
    except ValueError as e:
        print('Fetch failed')
        db.rollback()

    db.close()
    return member_vote


def db_find_project(project_name):
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql = """select * from PROJECT
                  where PROJECT_NAME = '%s'
                  """ % project_name

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except ValueError as e:
        print('Fetch failed')
        db.rollback()

    if result != ():
        db.close()
        return 1
    db.close()
    return 0


def project_existed(project_name):
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql = """select * from %s""" % project_name

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

    except ValueError as e:
        print('Fetch failed')
        db.rollback()

    if result != ():
        db.close()
        return 1
    else:
        db.close()
        return 0


def drop_table(project_name):
    db = pymysql.connect("localhost", "root", "jky594176", "project_member")
    cursor = db.cursor()
    sql = """delete from %s""" % project_name

    try:
        cursor.execute(sql)
        db.commit()

    except ValueError as e:
        print('Delete failed')
        db.rollback()

    db.close()

# def drop_table(project_name):



''' def add_namelist(name_list):
    list =[]
    return list 


def get_data(project_name):
    name = 1
    return name
    '''