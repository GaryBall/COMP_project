from DB_module import *
# 讨论结构是否合理，因为project和person的存储空间不同，而且也不需要用继承类。


class Project:

    # constructor
    def __init__(self, project_name, num_member, name_list):

        self.p_name = project_name
        self.number = num_member
        self.member_list = name_list

        add_project(project_name, num_member, name_list)
        create_person_table(project_name, name_list)

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

    def no_digit(self, str):
        '''if isinstance(str, 'int'):
            noDigit = False
            return noDigit
        else:
        这一块具体怎么写还有待商榷，我暂时要求输入的都是str类型，
        但是后面链接了数据库以后，输出的是什么类型，就应该按什么类型处理。
        如输入int？
        '''
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
        print(count, str_length)
        noDigit = bool(count == str_length)
        print(noDigit)
        return noDigit

    def __str__(self):
        return str(self.number) + ' ' + str(self.p_name)


class Person(Project):
    # constructor
    def __init__(self, project_name, member_name, vote_list):
        is_project = 0
        # super().__init__(self, project_name, num_member, name_list)

        self.m_name = member_name
        self.p_name = project_name
        self.vote = vote_list


    @property
    def m_name(self):
        return self._m_name

    @m_name.setter
    def m_name(self, the_name):
        if self.no_digit(the_name):
            self._m_name = the_name
        else:
            raise ValueError("Invalid member name" + the_name)


    @property
    def vote(self):
        _vote = get_vote_list(self.p_name, self.m_name)
        return self._vote

    @vote.setter
    def vote(self, thevote_list):
        if thevote_list != None:
            member_list = get_name_list(self.p_name)
            add_vote_list(self.p_name, self.m_name, member_list, thevote_list)
        else:
            raise ValueError("Invalid vote!")




