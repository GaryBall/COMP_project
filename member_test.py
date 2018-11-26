from member_module import project,person
from DB_module import *

def main():
    projectA = project('pA','5')
    print(projectA)
    theName = get_data(projectA.p_name)
    theVote = [1,2,3,4,5]
    #personA = person(projectA.p_name, projectA.number, theName, theVote)


if __name__  == "__main__":
    main()