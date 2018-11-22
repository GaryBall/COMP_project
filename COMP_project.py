from mainmenu_module import *


def main():

    establish_project()
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


if __name__ == '__main__':
    main()
