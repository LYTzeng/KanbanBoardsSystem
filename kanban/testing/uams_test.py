"""UAMS單元測試"""
import unittest
from kanban.UAMS.src.user import User
from kanban.testing.mock import Request
from kanban.firebase.setup import Firebase, Pyrebase


class TestUser(unittest.TestCase):
    firebase = Firebase()
    pyrebase = Pyrebase()
    # 建立一個假的Firebase User
    fakeClient = User(firebase, pyrebase)
    # 建立一個假的Django request
    request_generator = Request()

    def setUp(self):
        # 測試create()所需的User class
        self.client = self.fakeClient
        self.request = self.request_generator.generate()
        # 建立測試login()所需的假帳戶
        self.user_for_testing = self.fakeClient
        self.request_for_testing_user = self.request_generator.generate()
        testing_user_info = {
            'email': 'login.success@test.com',
            'meema': '123456',
            'name': 'test',
            'username': 'success123'
        }
        self.request_for_testing_user.POST = testing_user_info
        self.user_for_testing.create(self.request_for_testing_user)

    def tearDown(self):
        del self.client
        del self.request
        self.user_for_testing.delete_user(self.request_for_testing_user)
        del self.user_for_testing
        del self.request_for_testing_user
    
    def test_login(self):
        """測試登入"""
        data0 = {
            'email': 'login.fail@test.com',
            'meema': '123456'
        }
        self.request.POST = data0
        message = self.fakeClient.login(self.request)
        data1 = {
            'email': 'login.success@test.com',
            'meema': '123456'
        }
        self.request.POST = data1
        session = self.fakeClient.login(self.request)
        self.assertEqual('EMAIL_NOT_FOUND: login.fail@test.com', message)
        self.assertEqual('success123', session.session['username'])
        self.assertEqual('test', self.fakeClient.name)
        self.assertEqual('success123', self.fakeClient.username)

    def test_create(self):
        """測試建立使用者"""
        data = {
            'username': 'oscar1234',
            'name': 'Oscar Test',
            'email': 'existed@test.com',
            'meema': '123456'
        }
        self.request.POST = data
        session = self.fakeClient.create(self.request)
        self.assertEqual('oscar1234', session.session['username'])

    def test_sign_out(self):
        """測試登出"""
        data1 = {
            'email': 'login.success@test.com',
            'meema': '123456'
        }
        self.request.POST = data1
        self.fakeClient.login(self.request)
        signout_request = self.fakeClient.sign_out(self.request)
        with self.assertRaises(KeyError):
            print(signout_request.session[('idToken', 'localId', 'username')])
            self.fakeClient.sign_out(self.request)

    def test_authorize(self):
        """測試權限驗證"""
        data = {
            'email': 'login.success@test.com',
            'meema': '123456'
        }
        self.request.POST = data
        session = self.fakeClient.login(self.request)
        self.assertTrue(self.fakeClient.authorize(session.session['idToken'],session.session['localId']))

    def test_join_and_get_project(self):
        """測試將使用者加入專案 以及取得用戶所屬專案list"""
        self.user_for_testing.join_project('A9zmCsIcad4AqWwNx3T6')
        self.user_for_testing.join_project('O3cbdiiF8J2jRdM11rAD')
        expected = ['A9zmCsIcad4AqWwNx3T6', 'O3cbdiiF8J2jRdM11rAD']
        self.assertEqual(expected, self.user_for_testing.get_project_list())

    def test_resign_project(self):
        """測試使用者退出專案"""
        self.user_for_testing.join_project('O3cbdiiF8J2jRdM11rAD')
        self.assertEqual(['O3cbdiiF8J2jRdM11rAD'], self.user_for_testing.get_project_list())
        self.user_for_testing.resign_project('O3cbdiiF8J2jRdM11rAD')
        self.assertEqual([], self.user_for_testing.get_project_list())

if __name__ == "__main__":
    unittest.main()
