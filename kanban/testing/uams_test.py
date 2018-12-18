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
        print(session)
        self.assertEqual('success123', session.session['username'])

    def test_create(self):
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
        data = {
            'email': 'login.success@test.com',
            'meema': '123456'
        }
        self.request.POST = data
        session = self.fakeClient.login(self.request)
        self.assertTrue(self.fakeClient.authorize(session.session['idToken'],session.session['localId']))


if __name__ == "__main__":
    unittest.main()
