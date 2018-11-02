import pymysql
import pandas as pd
global DB_LEN
DB_LEN = 5                  # Global DB_LEN is mainly used in function add_project


def main():
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

    main_menu()


def main_menu():
    """
    Return the main menu of Splitit.
    Option should be chosen here.
    @return:
      - Option A will lead to show_explanation function.
      - Option C will lead to create_project function.
      - Option V will lead to enter_votes function.
      - Option S will lead to show_project function.
      - Choosing option Q will exit.
      - Entering a wrong letter will go to error function.
    """
    while 1:
        print('Welcome to Split-it\n')
        print('\tAbout\t\t\t\t(A)')
        print('\tCreate Project\t\t(C)')
        print('\tEnter Votes\t\t\t(V)')
        print('\tShow Project\t\t(S)')
        print('\tQuit\t\t\t\t(Q)')
        option = input('\n\tPlease choose an option:')

        if option == 'A':
            show_explanation()
        elif option == 'C':
            create_project()
        elif option == 'V':
            enter_votes()
        elif option == 'S':
            show_project()
        elif option == 'Q':
            exit()
        else:
            error()


def show_explanation():
    # Show the explanation interface.
    print('\nThis application offers rational solutions to everyday \n'
          'fair division problems, using methods that provide \n'
          'indisputable fairness guarantees. It will help teams \n'
          'easier to allocate the credit of a project.\n')


def create_project():
    # This function shows the create project interface.
    project_name = input('Enter the project name:')
    members_number = input('Enter the number of team members:')
    while not is_valid(members_number):
        # Test whether the number is valid.
        print('Please enter a valid value')
        members_number = input('Enter the number of team members:')

    members_number = int(members_number)
    while members_number <= 0:
        print('You can not enter a number under 0, please enter again!')
        members_number = int(input('Enter the number of team members:'))
    print('\n')
    member_list = []
    for i in range(1, members_number+1):
        member_name = input('\tEnter the name of team member {}:'.format(i))
        member_list.append(member_name)
        # Easy to pass parameters later.

    print('\n')

    add_project(project_name, members_number, member_list)

    input('Press <Enter> to return to the main menu:')
    print('\n')
    main_menu()


# Lazy evaluation
def is_valid(number):
    """
    This function will check if the number entered is valid.

    @param number: Number Entered
    @return: None
    """
    flag = is_int(number) and int(number) > 0
    return flag


def is_int(number):
    try:
        nb = int(number)  # If successfully transform string to int, return True
        return 1

    except ValueError as e:
        return 0  # Return False if failed


def enter_votes():
    return 0


def show_project():
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
            result = cursor.fetchall()      # fetch function return TUPLE
    finally:
        db.close()
    df = pd.DataFrame(list(result))         # Convert tuple to list, then DataFrame
    print(df)
    return 0


def error():
    """
    In main menu, if enter a wrong input, call this
    function, print error and return main menu.
    @return: None
    """
    print('\n')
    print('Error!please choose your option again')
    main_menu()


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


if __name__ == '__main__':
    main()
