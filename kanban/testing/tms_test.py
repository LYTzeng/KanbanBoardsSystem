import unittest
from kanban.TMS.src.task import Task
from kanban.PMS.src.project import Project
from kanban.testing.mock import Request
from kanban.firebase.setup import Firebase


class TestTask(unittest.TestCase):
    firebase = Firebase()
    # 建立一個假的Django request
    request_generator = Request()

    def setUp(self):
        # 測試用的專案
        self.project_id = 'owG3sOVuRZgXRo5hn4fw'
        self.fake_project = Project(self.firebase)
        self.request = self.request_generator.generate()
        name = "existed_project"
        owner = "success123"
        members = ['member1', 'member2']
        self.request.POST = {
            'name': name,
            'owner': owner,
            'members': members
        }
        self.fake_project.create(self.request)
        self.new_task = Task(self.firebase, self.project_id)  # 空的任務物件
        self.existed_task = Task(self.firebase, self.project_id)  # 測試已存在的任務
        self.request.POST = {
            'content': '撰寫STD',
            'owner': 'success123',
            'color': '#000000'
        }
        self.existed_task.add_task(self.request)

    def tearDown(self):
        self.fake_project.delete_project()
        del self.fake_project
        del self.request
        if self.new_task.get() != FileNotFoundError: self.new_task.del_task()
        del self.new_task
        if self.existed_task.get() != FileNotFoundError: self.existed_task.del_task()
        del self.existed_task

    def test_add_task(self):
        """測試建立任務"""
        self.request.POST = {
            'content': '建立test case',
            'owner': 'success123',
            'color': '#252525'
        }
        self.new_task.add_task(self.request)
        # 看看建立任務後 從資料庫抓下來是否正確
        self.new_task.get()
        self.assertEqual('建立test case', self.new_task.content)
        self.assertEqual('success123', self.new_task.owner)
        self.assertEqual('#252525', self.new_task.color)

    def test_del_task(self):
        """測試刪除任務"""
        self.assertEqual('撰寫STD', self.existed_task.get()["content"])  # 先驗證原本任務是存在的
        self.existed_task.del_task()
        self.assertEqual(FileNotFoundError, self.existed_task.get())  # 刪除後 驗證是否成功刪除

    def test_update(self):
        """測試更改任務內容"""
        self.request.POST = {
            'content': 'STD revise',
            'owner': 'success123',
            'color': '#878787'
        }  # 變更後 送出表單的內容
        self.existed_task.update(self.request)
        data = self.existed_task.get()
        # 看看DB那裏有沒有更新
        self.assertEqual('STD revise', data["content"])
        self.assertEqual('#878787', data["color"])

    def test_get(self):
        """測試 讓空的Task Class從資料庫取得現有任務狀態"""
        self.new_task.get(task_id=self.existed_task.task_id)
        self.assertEqual(self.existed_task.task_id, self.new_task.task_id)
        self.assertEqual(self.existed_task.content, self.new_task.content)
        self.assertEqual(self.existed_task.color, self.new_task.color)
        self.assertEqual(self.existed_task.start_time, self.new_task.start_time)
