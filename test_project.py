"""
This module is used for unittest.
In this module, class TextMainMenu is established to text our code.

setUp and tearDown methods are built to build environment for test and
recovery it after test due to our functions are connected to database,
so we do not want to change it after test.

We included 4 important function tests in this class, which can be extended
if necessary.

It is worth pointing out that unittest is probably failed in this stage because all
data in database is changed, so the parameters are completely different.
"""
import unittest
from DB_module import *
import mainmenu_module


class TestMainMenu(unittest.TestCase):

    def setUp(self):
        """
        To duplicate and build a new database to be used to test

        @return: None
        """
        print('Copying database.....\n preparing environment')
        db_list = []
        db = pymysql.connect("localhost", "root", "jky594176", "project_member")
        cursor = db.cursor()
        sql_show = "select * from PROJECT"
        try:
            cursor.execute(sql_show)
            result = cursor.fetchall()  # fetch function return TUPLE
            print('you have following projects:')
            for row in result:
                print(row[0])
                db_list.append(row[0])

        except ValueError as e:
            print("database show failed")
        sql_copy = "create table PROJECT_COPY select * from PROJECT"
        cursor.execute(sql_copy)
        for project_name in db_list:
            sql_copy = "create table %s_COPY select * from %s" % (project_name, project_name)
            cursor.execute(sql_copy)
        db.close()

    def tearDown(self):
        """
        To recovery it to origin after test. This includes delete
        the database and rename the packup database.
        @return:
        """
        print('deleting database.....\ncleaning up')
        db_list = []
        db = pymysql.connect("localhost", "root", "jky594176", "project_member")
        cursor = db.cursor()
        sql_show = "select * from PROJECT"
        try:
            cursor.execute(sql_show)
            result = cursor.fetchall()  # fetch function return TUPLE
            print('you have following projects:')
            for row in result:
                print(row[0])
                db_list.append(row[0])

        except ValueError as e:
            print("database show failed")
        sql_del = "drop table if exists PROJECT"
        cursor.execute(sql_del)
        sql_del = "rename table PROJECT_COPY to PROJECT"
        cursor.execute(sql_del)
        for project_name in db_list:
            sql_del = "drop table if exists %s" % (project_name)
            cursor.execute(sql_del)
            sql_del = "rename table %s_COPY to %s" % (project_name, project_name)
            cursor.execute(sql_del)
        db.close()

    def test_get_member_num(self):
        self.assertEqual(3, get_member_num('pA'))
        self.assertNotEqual(4, get_member_num('pA'))

    def test_db_find_project(self):
        self.assertEqual(1, db_find_project('pA'))

    def test_isvalid_num(self):
        self.assertEqual(1, mainmenu_module.isvalid_num(3))
        self.assertNotEqual(1, mainmenu_module.isvalid_num('gary'))

    def test_get_vote_list(self):
        self.assertEqual([0, 10, 90], get_vote_list('pA', 'gary'))

    def test_project_existed(self):
        self.assertEqual(1, project_voted('pA'))
        self.assertNotEqual(1, project_voted('PERSON'))


if __name__ == '__main__':
    unittest.main()
