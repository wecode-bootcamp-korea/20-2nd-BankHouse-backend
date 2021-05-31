import json
import bcrypt
import unittest
import jwt

from .models        import User, UserInformation
from my_settings    import SECRET_KEY, ALGORITHM
from .views         import KakaoLogInView
from django.test    import TransactionTestCase, Client
from unittest.mock  import patch, MagicMock


class KakaoLogInViewTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            email         = 'testemail@test.com',
            kakao_id      = '12345678',
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")               
    def test_kakao_login_success(self, mocked_requests):
        client  = Client()

        class MockedResponse:
            def json(self):                              
                return {
                    "id"            : "12345678",
                    "kakao_account" : {"email" : "testemail@test.com"}
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header              = {"HTTP_Authorization" : "access_token"}
        response            = client.get('/users/log-in/kakao', content_type='application/json', **header)
        login_token         = jwt.encode({'user_id': "12345678"}, SECRET_KEY, algorithm=ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message'      : 'SUCCESS', 
                'access_token' : login_token
            })
    
    @patch("users.views.requests") 
    def test_kakao_login_attribute_error(self, mocked_requests):
        client  = Client()

        class MockedResponse:
            def json(self):                              
                return {
                    "id"            : "12345678",
                    "kakao_account" : "",
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header              = {"HTTP_Authorization" : "access_token"}
        response            = client.get('/users/log-in/kakao', content_type='application/json', **header)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message": "INVALID_USER"
            })

    @patch("users.views.requests")  
    def test_kakao_login_invalid_user(self, mocked_requests):
        client  = Client()

        class MockedResponse:
            def json(self):                              
                return {
                    "id"            : "12345678",
                    "kakao_account" : {"email":"invalidemail@test.com"},
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header              = {"HTTP_Authorization" : "access_token"}
        response            = client.get('/users/log-in/kakao', content_type='application/json', **header)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "message": "INVALID_USER"
            })

    @patch("users.views.requests")  
    def test_kakao_login_key_error(self, mocked_requests):
        client  = Client()

        class MockedResponse:
            def json(self):                              
                return {
                    "properties" : {"nickname":"kakaotest"},
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header              = {"HTTP_Authorization" : "access_token"}
        response            = client.get('/users/log-in/kakao', content_type='application/json', **header)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "KEY_ERROR"
            })