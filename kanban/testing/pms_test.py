import unittest
from kanban.PMS.src.project import Project
from kanban.UAMS.src.user import User
from kanban.testing.mock import Request
from kanban.firebase.setup import Firebase, Pyrebase


class TestProject(unittest.TestCase):
    firebase = Firebase()
    pyrebase = Pyrebase()
    # 建立一個假的Django request
    request_generator = Request()
    fakeClient = User(firebase, pyrebase)

    def setUp(self):
        # 測試create()所需的User class
        # 建立一個假的Firebase User
        self.new_project = Project(self.firebase)
        self.old_project = Project(self.firebase)
        self.existed_project = Project(self.firebase)
        self.request = self.request_generator.generate()

        self.owner = self.fakeClient
        user_info = {
            'email': 'owner@test.com',
            'meema': '123456',
            'name': 'mister owner',
            'username': 'owner123'
        }
        self.request.POST = user_info
        self.owner.create(self.request)
        self.member1 = self.fakeClient
        user_info = {
            'email': 'member1.test@test.com',
            'meema': '123456',
            'name': 'member one',
            'username': 'member1'
        }
        self.request.POST = user_info
        self.member1.create(self.request)

        name = "existed_project"
        owner = "owner123"
        members = 'owner123'
        self.request.POST = {
            'name': name,
            'owner': owner,
            'members': members
        }
        self.existed_project.create(self.request)
        self.existed_project_id = self.existed_project.project_id

    def tearDown(self):
        if self.new_project.project_document is not None:
            self.new_project.delete_project()
        del self.new_project
        self.existed_project.delete_project()
        del self.existed_project
        del self.existed_project_id
        del self.request
        self.owner.delete_user()
        self.member1.delete_user()
        del self.owner
        del self.member1
        del self.old_project

    def test_create(self):
        name = "test_create_project"
        owner = "owner123"
        members = 'owner123'
        self.request.POST = {
            'name': name,
            'owner': owner,
            'members': members
        }
        self.new_project.create(self.request)
        project_id = self.new_project.project_id
        self.assertEqual(name, self.new_project.name)
        self.assertEqual(owner, self.new_project.owner)
        self.new_project.get_board(project_id=self.new_project.project_id)
        self.assertEqual(name, self.new_project.name)
        self.assertEqual(owner, self.new_project.owner)
        self.assertEqual(project_id, self.new_project.project_id)

    def test_add_members(self):
        members_to_add = 'member1'
        self.request.POST = {
            'member-to-add': members_to_add
        }
        self.existed_project.add_member(self.request)
        expected = ['owner123', 'member1']
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual(expected, self.existed_project.members)

    def test_delete_member(self):
        member_to_delete = 'member1'
        self.request.POST = {
            'member-to-delete': member_to_delete
        }
        self.existed_project.delete_member(self.request)
        expected = ['owner123']
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual(expected, self.existed_project.members)

    def test_rename(self):
        new_name = 'project one'
        self.request.POST = {'new-name': new_name}
        self.existed_project.rename(self.request)
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual(new_name, self.existed_project.name)

    def test_get_board(self):
        existed_project_id = self.existed_project.project_id
        self.old_project.get_board(project_id=existed_project_id)
        self.assertEqual(self.existed_project.name, self.old_project.name)
        self.assertEqual(self.existed_project.owner, self.old_project.owner)
        self.assertEqual(self.existed_project.columns, self.old_project.columns)
        self.assertEqual(self.existed_project.members, self.old_project.members)
        self.assertEqual(self.existed_project_id, self.old_project.project_id)

    def test_move_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'Todo')
        self.existed_project.add_task('O3cbdiiF8J2jRdM11rAD', 'Todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.existed_project.move_task('A9zmCsIcad4AqWwNx3T6', 'Todo', 'In Progress')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['In Progress'][0])

    def test_add_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'Todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['Todo'][0])

    def test_del_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'Todo')
        self.existed_project.add_task('O3cbdiiF8J2jRdM11rAD', 'Todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('O3cbdiiF8J2jRdM11rAD', self.existed_project.columns['Todo'][1])
        self.existed_project.del_task('O3cbdiiF8J2jRdM11rAD', 'Todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['Todo'][0])


if __name__ == "__main__":
    unittest.main()
