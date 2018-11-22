from DB_module import *

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
        nb = int(number)         # If successfully transform string to int, return True
        return 1

    except ValueError as e:
        return 0            # Return False if failed


def enter_votes():
    return 0


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
