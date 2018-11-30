from member_module import Project,Person
from DB_module import *
from mainmenu_module import *

def main():

    a = db_find_project('pA')
    print(a)

if __name__  == "__main__":
    main()