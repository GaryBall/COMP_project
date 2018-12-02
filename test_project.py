import unittest
from DB_module import *
import mainmenu_module

member_list = ['Gary', 'Alex', 'Aria', 'Anna', 'Yuanhao', 'Frank']
# create_person_table('Gary', member_list)


class TestMainMenu(unittest.TestCase):

    def setUp(self):
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
        sql_copy = ("create table PROJECT_COPY select * from PROJECT")
        cursor.execute(sql_copy)
        for project_name in db_list:
            sql_copy = ("create table %s_COPY select * from %s") % (project_name, project_name)
            cursor.execute(sql_copy)
        db.close()

    def tearDown(self):
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
        sql_del = ("drop table if exists PROJECT")
        cursor.execute(sql_del)
        sql_del = ("rename table PROJECT_COPY to PROJECT")
        cursor.execute(sql_del)
        for project_name in db_list:
            sql_del = ("drop table if exists %s") % (project_name)
            cursor.execute(sql_del)
            sql_del = ("rename table %s_COPY to %s") % (project_name, project_name)
            cursor.execute(sql_del)
        db.close()

    def test_get_member_num(self):
        self.assertEqual(3,get_member_num('pA'))
        self.assertNotEqual(4,get_member_num('pA'))

    def test_db_find_project(self):
        self.assertEqual(1, db_find_project('pA'))

    def test_isvalid_num(self):
        self.assertEqual(1, mainmenu_module.isvalid_num(3))
        self.assertNotEqual(1, mainmenu_module.isvalid_num('gary'))

    def test_get_vote_list(self):
        self.assertEqual([0, 10, 90], get_vote_list('pA', 'gary'))

    def test_project_existed(self):
        self.assertEqual(1, project_existed('pA'))
        self.assertNotEqual(1, project_existed('PERSON'))


if __name__ == '__main__':
    str = "      "
    print(1 and 1 and 1)
    # unittest.main()
