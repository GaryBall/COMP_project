from member_module import Project, Person
from DB_module import *
import calculate_vote as cv
import re
import mainmenu_module as mainmenu


def file_input(file_name):
    """
    Read information from the external file.
    This function initialize the projects by line in file.
    If an error is found in one line, this line will be dropped but others will not be influenced.
    @return:
    """

    # flag1 is the mark to detect errors for the whole file
    flag1 = 1
    fd = open('../COMP_project/'+file_name, 'r+')
    line = fd.readline().rstrip()
    while line != "":
        line_list = re.split(", | ,|,| ", line)
        # check the format

        # flag2 is the mark to detect error for every line
        flag2 = format_check(line_list)
        if not flag2:
            flag1 = 0
            line = fd.readline().rstrip()
            continue

        member_number = int(line_list[1])
        name_list = line_list[2:(2 + member_number)]
        # check if repeated names appear in member list.
        if check_repeat(name_list):
            pass
        else:
            print("Please check if the member names are repeated in %s." % line_list[0])
            flag1 = 0
            line = fd.readline().rstrip()
            continue

        project_class = Project(line_list[0], member_number, name_list)
        mainmenu.project_list.append(project_class)

        vote_list = [0 for _ in range(member_number)]

        # detect some unexpected errors, e.g. some spelling mistake.
        for i in range(member_number):
            for j in range(member_number):
                if line_list[2-j+(2*j+1)*member_number] == name_list[i]:
                    vote_list[i] = line_list[(2-j+(2*j+1)*member_number):(1-j)+(2*j+3)*member_number]
                elif line_list[2-j+(2*j+1)*member_number] not in name_list:
                    print("An unexpected name appear in the file, please check the correction of file!")
                    flag1 = 0
                    flag2 = 0
                else:
                    pass
        # generate a vote dictionary to arrange the sequence of input
        vote_dict = {}
        for i in range(member_number):
            vote_dict[name_list[i]] = [0 for _ in range(member_number)]
            for ii in range(1, len(vote_list[i])):
                for k in range(member_number):
                    if ii % 2 == 1 and vote_list[i][ii] == name_list[k]:
                        try:
                            vote_dict[name_list[i]][k] = int(vote_list[i][ii+1])
                        except ValueError as e:
                            print("File format error! Can't get file input for %s" % line_list[0])
                            flag1 = 0
                            flag2 = 0
        # "flag2 == 0" means errors is found in this line, person class will not be established.
        if flag2:
            if not est_person_class(name_list, vote_dict, line_list):
                flag1 = 0

        line = fd.readline().rstrip()

    # if flag1 equals to 0,
    if flag1 == 0:
        print("\nError generated in importing file, information is dropped,\n"
              "but you still can create your own project of other lines.")

    fd.close()


def file_output(project_list_db):
    """
    Write to an output file.

    @type project_list_db: tuple
    @param project_list_db: The list of projects from database, row[0] is the project name,
    row[1] is the member number.
    @return:
    """
    fd = open('../COMP_project/spliddit.txt', 'w+')
    member_num = []
    for row in project_list_db:
        member_num.append(int(row[1]))
    max_num = max(member_num)
    est_vote_table(max_num)

    for row in project_list_db:
        project_name = row[0]
        name_list = get_name_list(project_name)

        fd.write(project_name)
        name_str = ""
        for member in name_list:
            name_str += ",%s" % str(member)
        fd.write(","+str(len(name_list))+name_str)
        for member in name_list:
            vote_list = get_vote_list(project_name, member)
            if vote_list != []:
                fd.write(','+member)
                for i in range(len(name_list)):
                    if name_list[i] == member:
                        continue
                    else:
                        fd.write(',%s,%d' % (name_list[i], vote_list[i]))
            else:
                break
        fd.write('\n')
        vote_result = cv.calculate_vote(project_name)
        # output allocation result
        if vote_result:
            vote_to_db(project_name, name_list, vote_result*100)

        else:
            print("You haven't voted for some existing project. Can't get file output.")

    fd.close()


def est_person_class(name_list, vote_dict, line_list):
    """
    establish people's class for each project.

    @type: name_list: list
    @param name_list: members' name list
    @type: vote_dict: dictionary
    @param vote_dict: member's vote dictionary
    @type: line_list: list
    @param line_list: All the information of this line.
    @return:
    """
    flag1 = 1
    for name in name_list:
        if add_to_100(vote_dict[name]):
            person_class = Person(line_list[0], name, vote_dict[name])
            mainmenu.member_class_list.append(person_class)
        else:
            print("Vote list error in %s!" % line_list[0])
            flag1 = 0
            break
    return flag1


def add_to_100(number_list):
    """
    Check if the votes from members adds up to 100.
    @type number_list: list
    @param number_list:
    @return: The result of the checking
    """
    count = 0
    for number in number_list:
        if number >= 0:
            count += number
        else:
            return 0

    if count == 100:
        return 1
    else:
        return 0


def check_equal(number, line_length):
    """
    check whether the number provided is equal to length of name_list
    According to our calculation, if a project contains n members, the length of the line should be (2*n^2+2)

    @type number: int
    @param number: the member number of the project
    @type line_length: int
    @param line_length: the length of the line.
    @return: Checking result
    """

    expect_length = 2*number*number+2
    if expect_length == line_length:
        return 1
    else:
        return 0


def check_repeat(name_list):
    """
    Check if the names of members are duplicated.
    @type name_list: list
    @param name_list: the name list of members
    @return: Checking result
    """

    name_set = set(name_list)
    if len(name_list) != len(name_set):
        return 0
    else:
        return 1


def format_check(line_list):
    """
    Check the format of the line is correct. Invalid format include repeated project name, correct member provided
    and proper position of specific element.

    @type line_list: list
    @param line_list:
    @return:
    """
    # unfinished
    # check if there are repeated project names
    for project in mainmenu.project_list:
        if line_list[0] == project.p_name:
            print("project name \'%s\' is duplicated!" % line_list[0])
            return 0
        if not Project.no_digit(line_list[0]) or line_list[0].isspace():
            print('Project name \'%s\' is not valid' % line_list[0])
            return 0
    try:
        # Check the second element in line_list is a integer cause this should be the member number.
        member_number = int(line_list[1])
    except ValueError as e:
        print("Did you provide the number of members in %s?" % line_list[0])
        return 0

    # check if the line length is proper.
    if not check_equal(member_number, len(line_list)):
        print("Please check if the number provided is equal to name list in %s." % line_list[0])
        return 0

    return 1


def main():

    # mainmenu.exit_project()
    file_input()


if __name__ == '__main__':
    main()
