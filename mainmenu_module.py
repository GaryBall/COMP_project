from DB_module import *
from member_module import Project, Person
import fileIO
import calculate_vote as cv


def show_explanation():
    # Show the explanation interface, as well as some suggestion for users
    print('\nThis application offers rational solutions to everyday \n'
          'fair division problems, using methods that provide \n'
          'indisputable fairness guarantees. It will help teams \n'
          'easier to allocate the credit of a project.\n'
          'Please make sure that everything you enter do not\n'
          'contain key words in MYSQL like as, into, and you\n'
          'are not supposed to enter a name more than 20 letters')


# A global list to store all the project classes.
project_list = []


# The minimum of member number. We do not set maximum because we think it's unnecessary
MINIMUM = 3


def create_project():
    global MINIMUM
    # This function shows the create project interface.
    project_name = input('Enter the project name:')
    while db_find_project(project_name):
        print("This project name is occupied!")
        project_name = input("Choose another project name")

    while not Project.no_digit(project_name) or project_name.isspace():
        print('Your project name is not valid')
        project_name = input('Enter the project name:')

    members_number = input('Enter the number of team members:')
    while not isvalid_num(members_number):
        # Test whether the number is valid.
        print('Please enter a valid value')
        members_number = input('Enter the number of team members:')

    members_number = int(members_number)
    while members_number < MINIMUM:
        print('You can not enter a number under 3, please enter again!')
        members_number = int(input('Enter the number of team members:'))
    print('\n')

    member_list = []
    for i in range(1, members_number+1):
        member_name = input('\tEnter the name of team member {}:'.format(i))
        while not Project.no_digit(member_name) or member_name.isspace():
            print('Your project name is not valid')
            member_name = input('\tEnter the name of team member {}:'.format(i))
        while member_name in member_list:
            print("{} has already been a member!".format(member_name))
            member_name = input('\tPlease enter a different name of team member {}:'.format(i))
        member_list.append(member_name)
        # Easy to pass parameters later.

    print('\n')
    global project_list
    project_list.append(Project(project_name, members_number, member_list))

    input('Press <Enter> to return to the main menu:')
    print('\n')


# Lazy evaluation
def isvalid_num(number):
    """
    This function will check if the number entered is valid.

    @param number: Number Entered
    @return: None
    """
    flag = is_int(number) and int(number) > 0
    return flag


def is_int(number):
    try:
        nb = int(number)         # If successfully transform string to int, return True
        return 1

    except ValueError as e:
        return 0            # Return False if failed


# This is a global list built for store Person class.
member_class_list = []


def enter_votes():
    """
    This function is for members to enter votes for
    the other members in existing projects.

    @return:None
    """
    flag = 0
    if DB_show_project() == ():
        flag = 1

    while flag == 0:
        # Here we show all the existing projects that are able to be chosen.
        print("You now have following project:")
        result = DB_show_project()
        for row in result:
                print(row[0])
        project_name = input('Enter project name:')
        # connect to class Project to get name list

        # make sure that project name is valid
        if db_find_project(project_name):
            if project_voted(project_name):
                choice = input("***Warning: The project you chose have been voted, "
                               "enter D - you can drop you previous vote\n"
                               "enter any other key to give up vote")
                if choice == 'D':
                    drop_table(project_name)
                else:
                    break
            flag = 1
            member_list = get_name_list(project_name)
            members_number = len(member_list)
            print('There are {} team members.'.format(members_number))
            print('\n')
            global member_class_list
            for member_name in member_list:
                vote_list = []
                while True:
                    print("Enter {}'s votes, points must add up to 100:".format(member_name))
                    count = 0
                    for second_name in member_list:
                        if second_name != member_name:
                            while True:
                                thevote = input("\tEnter {}'s points for {}:\t".format(member_name, second_name))
                                if thevote.isdigit():
                                    thevote_int = int(thevote)
                                    count += thevote_int
                                    vote_list.append(thevote)
                                    break
                                else:
                                    print("***Error: Votes must be integers. Please Enter "
                                          "{}'s points for {} again.".format(member_name, second_name))
                                    continue
                                    # If a vote is not integer, will ask him/her to enter this particular vote again.
                        else:
                            vote_list.append('0')
                    if count == 100:
                        # check whether the sum of the votes is 100 or not.
                        break
                    else:
                        print('\n')
                        print("***Error: Points must add up to 100. Please Enter {}'s votes again.".format(member_name))
                        vote_list = []
                        continue
                        # If not equals 100, will need to enter his/her vote for all other members again.

                person = Person(project_name, member_name, vote_list)
                member_class_list.append(person)

                print('\n')
        else:
            print('\n')
            print('No such project. Enter another project name')

    input('Press <Enter> to return to the main menu:')
    print('\n')


def exit_project():
    """
    before exiting project, we need to call file_output to output file.

    @return:
    """

    project_list_db = DB_show_project()
    if project_list_db != ():
        try:
            fileIO.file_output(project_list_db)
        except KeyError as e:
            print("You haven't voted for existing projects. Can't get file output.")
    db_close()
    exit()


def show_project():
    """
    call DB_show to get project data from class. At this stage,
    you can find the project name and vote result of it.

    DB_show() is a function directly get data from database, but it's commented now
    because we write a way to access.

    @return: None
    """
    global project_list
    global member_class_list
    project_name_list = []
    if project_name_list is None:
        print('You haven\'t voted')
    elif project_list == []:
        print("You haven't established any project")
    else:
        for project in project_list:
            print(project)
            project_name_list.append(project.p_name)

        choice = input("Enter the project name from above:")
        print("\n")
        while choice not in project_name_list:
            # if user enter a choice not in project_name_list,
            choice = input("No such project! Enter again:")
            # flag is assigned to 1 when a person class is successfully found.
        flag = 0
        voted = 0
        for i in range(len(member_class_list)):
            if member_class_list[i].p_name == choice:
                voted = 1
                break
        if voted:
            allocation = cv.calculate_vote(choice)
        j = 0
        for i in range(len(member_class_list)):
            if member_class_list[i].p_name == choice:
                flag = 1
                print('\t%s:\t%.2f' % (member_class_list[i].m_name, allocation[j]*100))
                j += 1
        else:
            if flag == 0:
                print("You haven't voted")

    input("\npress <Enter> to return the main menu:")
    # DB_show()
    return 0


def error():
    """
    In main menu, if enter a wrong input, call this
    function, print error and return main menu.
    @return: None
    """
    print('\n')
    print('Error!please choose your option again')
