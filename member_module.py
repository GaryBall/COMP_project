"""
At first we wanted to establish a class Person inherited from Project. However,
this is not a valid way because this is a waste of storage space (We have to store
data like project_name twice. So we give up this idea and have two class:
Class Project with the attributes p_name, number
)
"""
from DB_module import *


class Project:
    """
    Project class includes attribute: p_name, number, member_list, which will
    also be stored into database. A static method no_digt to judge if the validation
    of entering content. p_name and number are stored in class, while member_list is
    stored in database and its getter directly connected to database.
    """

    # constructor
    def __init__(self, project_name, num_member, name_list):

        add_project(project_name, num_member, name_list)
        create_person_table(project_name, name_list)

        self.p_name = project_name
        self.number = num_member
        self.member_list = name_list

    @property
    def member_list(self):
        self._member_list = get_name_list(self.p_name)
        return self._member_list

    @member_list.setter
    def member_list(self, the_namelist):
        _member_list = the_namelist
        # add_namelist(the_namelist)

    @property
    def number(self):
        # get_member_num use PyMysql to get the value from database
        # self._number = get_member_num(self._p_name)
        return self._number

    @number.setter
    def number(self, theNumber):
        if not self.no_digit(theNumber):
            self._number = theNumber
            # add_member_num use PyMysql to add the value to database
            # add_member_num(self.p_name, theNumber)
        else:
            raise ValueError("Invalid member number " + theNumber)

    @property
    def p_name(self):
        return self._p_name

    @p_name.setter
    def p_name(self, the_name):
        if self.no_digit(the_name):
            self._p_name = the_name

        else:
            raise ValueError("Invalid project name " + the_name)

    @staticmethod
    def no_digit(str):
        """
        no_digit can judge if a string contain number (like int, float)
        """
        if isinstance(str, int):
            noDigit = False
            return noDigit
        str_length = len(str)
        count = 0
        for letter in str:
            try:
                float(letter)
            except ValueError as e:
                count += 1
                continue
        noDigit = bool(count == str_length)
        return noDigit

    def __str__(self):
        return str(self.p_name) + ' contains ' + str(self.number) + ' members, they are:'\
               + str(self.member_list)


class Person:
    """
    Person class has attributes including m_name, p_name, vote. vote data will be
    store into databse while setting and get directly from database because it's large
    and costs too much space in memory. While p_name and m_name are stored in class because
    it's little.
    """

    # constructor
    def __init__(self, project_name, member_name, vote_list):

        self.m_name = member_name
        self.p_name = project_name
        self.vote = vote_list

    @property
    def m_name(self):
        return self._m_name

    @m_name.setter
    def m_name(self, the_name):
        if Project.no_digit(the_name):
            self._m_name = the_name
        else:
            raise ValueError("Invalid member name" + the_name)

    @property
    def vote(self):
        # get votes list from database.
        self._vote = get_vote_list(self.p_name, self.m_name)
        return self._vote

    @vote.setter
    def vote(self, thevote_list):
        if thevote_list is not None:
            member_list = get_name_list(self.p_name)
            # send vote list to database
            add_vote_list(self.p_name, self.m_name, member_list, thevote_list)
        else:
            raise ValueError("Invalid vote!")

    @property
    def p_name(self):
        return self._p_name

    @p_name.setter
    def p_name(self, the_pj_name):
        if Project.no_digit(the_pj_name):
            self._p_name = the_pj_name
        else:
            raise ValueError("Invalid project name " + the_pj_name)

    def __str__(self):
        return str(self.m_name) + ' belongs to ' + str(self.p_name)+\
               ', here are his votes to others: ' + str(self.vote)
