from mainmenu_module import *
import fileIO as fIO
import os


def main():
    establish_project()
    print("You can import former project by file")
    print("Enter (Y) to import former project")
    choice = input("Enter any other key to start as a beginner.")
    if choice == 'Y':
        file_name = get_file()
        if file_name:
            fIO.file_input(file_name)

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
        print('\tAbout\t\t\t(A)')
        print('\tCreate Project\t\t(C)')
        print('\tEnter Votes\t\t(V)')
        print('\tShow Project\t\t(S)')
        print('\tQuit\t\t\t(Q)')
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
            exit_project()
        else:
            error()


def get_file():
    """
    get the file existing in pathway right now,
    and let the user select a file to open
    @return: the selected file
    """
    path = "../COMP_project"
    files_in_path = os.listdir(path)
    flag = 0
    for file in files_in_path:
        if os.path.splitext(file)[1] == ".txt":
            print(file)
            flag = 1

    if flag == 1:
        file_selected = input('\n\tPlease choose a file:')
        while file_selected not in files_in_path:
            file_selected = input('\n\tNo such file,Please choose another file:')

        return file_selected
    else:
        print("No file found")
        return 0


if __name__ == '__main__':
    main()
