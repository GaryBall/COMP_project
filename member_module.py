class project():



    # constructor
    def __init__(self,project_name,num_member):
        self.p_name = project_name
        self.number = num_member


    @property
    def p_name(self):
        return self._p_name

    @p_name.setter
    def p_name(self, theName):
        if not self.containDigit(theName):
            self._p_name  = theName
        else:
            raise ValueError("Invalid project name" + theName)

    def containDigit(str):
        noDigit = True
        for letter in str:
            try:
                float(letter)
                noDigit = False
                break
            except ValueError as e:
                continue
        return noDigit




def person(project):
    # constructor
    def __init__(self,project_name,num_member,member_name):
        project.__init__(self, project_name ,num_member)

        self.m_name = member_name


    @property
    def m_name(self):
        return self._m_name

    @m_name.setter
    def m_name(self, theName):
        if not self.containDigit(theName):
            self._m_name = theName
        else:
            raise ValueError("Invalid member name" + theName)





