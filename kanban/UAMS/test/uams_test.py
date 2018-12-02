"""UAMS單元測試
專案根目錄> python -m unittest -v kanban\UAMS\test\uams_test.py -b
"""
import unittest
from ..src.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        from django.http import HttpRequest
        from KB import settings as st
        from django.conf import settings
        settings.configure(
            DEBUG=True,
            TEMPLATE_DEBUG=True,
            DATABASES=st.DATABASES,
            INSTALLED_APPS=st.INSTALLED_APPS,
            MIDDLEWARE_CLASSES=st.MIDDLEWARE_CLASSES
        )
        from django.contrib.sessions.middleware import SessionMiddleware
        self.request = HttpRequest()
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.fakeUser = User()

    def tearDown(self):
        del self.fakeUser
        del self.request

    def test_login(self):
        data0 = {
            'email': 'login.fail@test.com',
            'meema': '123456'
        }
        self.request.POST = data0
        message = self.fakeUser.login(self.request)
        excepted_message = 'EMAIL_NOT_FOUND'
        data1 = {
            'email': 'login.success@test.com',
            'meema': '123456'
        }
        self.request.POST = data1
        session = self.fakeUser.login(self.request)
        expected_username = 'success123'
        self.assertEqual(excepted_message, message)
        self.assertEqual(expected_username, session.session['username'])

    # def test_create(self):
    #     data = {
    #         'username': 'oscar1234',
    #         'name': 'Oscar Test',
    #         'email': 'existed@test.com',
    #         'meema': '123456'
    #     }
    #     req = requests.post('/', data=data)


if __name__ == "__main__":
    unittest.main()