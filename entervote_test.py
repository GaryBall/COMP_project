from DB_module import *

project_name = input('Enter project name:')

# 此处外接Project class 获得member list

member_list = get_name_list('pA')
members_number = len(member_list)
print(member_list)


def enter_votes():
    project_name_enter = input('Enter the project name:')
    if project_name_enter == project_name:
        print('There are {} team members.'.format(members_number))
        print('\n')
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
            print(vote_list)
            # 此处通过member_list 创建Person class
            print('\n')
    else:
        print('\n')
        print('No such project.')

    input('Press <Enter> to return to the main menu:')
    print('\n')


enter_votes()