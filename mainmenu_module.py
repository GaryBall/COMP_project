from DB_module import *
from member_module import Project, Person


MINIMUM = 3


def show_explanation():
    # Show the explanation interface.
    print('\nThis application offers rational solutions to everyday \n'
          'fair division problems, using methods that provide \n'
          'indisputable fairness guarantees. It will help teams \n'
          'easier to allocate the credit of a project.\n')


def create_project():
    global MINIMUM
    # This function shows the create project interface.
    project_name = input('Enter the project name:')
    if isvalid_name(project_name):
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
        member_list.append(member_name)
        # Easy to pass parameters later.

    print('\n')

    projectA = Project(project_name, members_number, member_list)

    input('Press <Enter> to return to the main menu:')
    print('\n')


def isvalid_name(name):
    return 0

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


def enter_votes():
    project_name = input('Enter project name:')
    # 输错p_name还要改

    # connect to class Project to get name list

    # make sure that project name is valid
    if db_find_project(project_name):
        member_list = get_name_list(project_name)
        members_number = len(member_list)
        print(member_list)
        print('There are {} team members.'.format(members_number))
        print('\n')
        member_class_list = []
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
                                print("***Error: Votes must be integers. Please Enter {}'s points for {} again.".format(
                                    member_name, second_name))
                                continue
                    else:
                        vote_list.append('0')
                if count == 100:
                    break
                else:
                    print('\n')
                    print("***Error: Points must add up to 100. Please Enter {}'s votes again.".format(member_name))
                    vote_list = []
                    continue

            person = Person(project_name, member_name, vote_list)
            member_class_list.append(person)
            print(member_class_list)

            print('\n')
    else:
        print('\n')
        print('No such project.')

    input('Press <Enter> to return to the main menu:')
    print('\n')


def show_project():
    DB_show()
    return 0


def error():
    """
    In main menu, if enter a wrong input, call this
    function, print error and return main menu.
    @return: None
    """
    print('\n')
    print('Error!please choose your option again')
