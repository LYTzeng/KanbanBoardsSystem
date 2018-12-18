import unittest
from kanban.PMS.src.project import Project
from kanban.testing.mock import Request
from kanban.firebase.setup import Firebase


class TestProject(unittest.TestCase):
    firebase = Firebase()
    # 建立一個假的Django request
    request_generator = Request()

    def setUp(self):
        # 測試create()所需的User class
        # 建立一個假的Firebase User
        self.new_project = Project(self.firebase)
        self.existed_project = Project(self.firebase)
        self.request = self.request_generator.generate()
        name = "existed_project"
        owner = "success123"
        members = ['member1', 'member2']
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

    def test_create(self):
        name = "test_create_project"
        owner = "success123"
        self.request.POST = {
            'name': name,
            'owner': owner
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
        members_to_add = ['member3', 'member4']
        self.request.POST = {
            'members-to-add': members_to_add
        }
        self.existed_project.add_members(self.request)
        expected = ['member1', 'member2', 'member3', 'member4']
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual(expected, self.existed_project.members)

    def test_delete_member(self):
        member_to_delete = 'member1'
        self.request.POST = {
            'member-to-delete': member_to_delete
        }
        self.existed_project.delete_member(self.request)
        expected = ['member2']
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
        self.request.POST = {'project-id': existed_project_id}
        self.new_project.get_board(self.request)
        self.assertEqual(self.existed_project.name, self.new_project.name)
        self.assertEqual(self.existed_project.owner, self.new_project.owner)
        self.assertEqual(self.existed_project.columns, self.new_project.columns)
        self.assertEqual(self.existed_project.members, self.new_project.members)
        self.assertEqual(self.existed_project_id, self.new_project.project_id)

    def test_move_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'todo')
        self.existed_project.add_task('O3cbdiiF8J2jRdM11rAD', 'todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.existed_project.move_task('A9zmCsIcad4AqWwNx3T6', 'todo', 'progress')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['progress'][0])

    def test_add_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['todo'][0])

    def test_del_task(self):
        self.existed_project.add_task('A9zmCsIcad4AqWwNx3T6', 'todo')
        self.existed_project.add_task('O3cbdiiF8J2jRdM11rAD', 'todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('O3cbdiiF8J2jRdM11rAD', self.existed_project.columns['todo'][1])
        self.existed_project.del_task('O3cbdiiF8J2jRdM11rAD', 'todo')
        self.existed_project.get_board(project_id=self.existed_project_id)
        self.assertEqual('A9zmCsIcad4AqWwNx3T6', self.existed_project.columns['todo'][0])


if __name__ == "__main__":
    unittest.main()
