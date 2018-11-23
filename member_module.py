from DB_module import *
# 讨论结构是否合理，因为project和person的存储空间不同，而且也不需要用继承类。

class project():

    # constructor
    def __init__(self, project_name, num_member):
        self.p_name = project_name
        self.number = num_member


    @property
    def number(self):
        # get_member_num use PyMysql to get the value from database
        self._number = get_member_num(self._p_name)
        return self._number

    @number.setter
    def number(self, theNumber):
        if not self.no_digit(theNumber):
            # add_member_num use PyMysql to add the value to database
            add_member_num(theNumber)
        else:
            raise ValueError("Invalid member number " + theNumber)

    @property
    def p_name(self):
        return self._p_name

    @p_name.setter
    def p_name(self, theName):
        if self.no_digit(theName):
            self._p_name = theName

        else:
            raise ValueError("Invalid project name " + theName)

    def no_digit(self, str):
        '''if isinstance(str, 'int'):
            noDigit = False
            return noDigit
        else:
        这一块具体怎么写还有待商榷，我暂时要求输入的都是str类型，
        但是后面链接了数据库以后，输出的是什么类型，就应该按什么类型处理。
        如输入int？
        '''
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


class person(project):
    # constructor
    def __init__(self, project_name, num_member, member_name, vote_list):
        project.__init__(self, project_name, num_member)

        self.m_name = member_name
        self.vote = vote_list

    @property
    def m_name(self):
        return self._m_name

    @m_name.setter
    def m_name(self, theName):
        if self.no_digit(theName):
            self._m_name = theName
        else:
            raise ValueError("Invalid member name" + theName)



    @property
    def vote(self):
        return self._vote

    @vote.setter
    def vote(self,vote_list):
        if vote_list != None:
            _vote = vote_list
        else:
            raise ValueError("Invalid vote!")

