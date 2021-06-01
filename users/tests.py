import json
import bcrypt
import unittest
import jwt

from .models        import User, UserInformation
from my_settings    import SECRET_KEY, ALGORITHM
from .views         import KakaoLogInView
from django.test    import TestCase, TransactionTestCase, Client
from unittest.mock  import patch, MagicMock


class KakaoLogInViewTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            email         = 'testemail@test.com',
            kakao_id      = '12345678',
        )

class SignUpViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email       = "testemail@test.com",
            password    = "testpassword",
        )
        UserInformation.objects.create(
            user_id     = user.id,
            nickname    = "testnickname",
            is_expert   = True,
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
        UserInformation.objects.all().delete()

    def test_signup_post_success(self):    
        client       = Client()
        test_data = {
            "email"       : "testemail123@test.com",
            "password"    : "testpassword12",
            "nickname"    : "testnickname123",
            "is_expert"   : True,
        }
        response=client.post('/users/sign-up',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            "message": "SUCCESS",
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTR9.mxIXTHn404G6eZZftbtrqK7Oeva3cPaYKlvQ_iAR0KA",
            })
        

    def test_signup_post_invalid_email(self):
        client     = Client()
        test_data = {
            "email"       : "testemailcom",
            "password"    : "12345678",         
            "nickname"    : "testnickname12",
            "is_expert"   : True,
        }
        response=client.post('/users/sign-up',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message" : "INVALID_EMAIL"
        })

    def test_signup_post_invalid_password(self):
        client     = Client()
        test_data = {
            "email"       : "test01@gmail.com",
            "password"    : "test",         
            "nickname"    : "testnickname12",
            "is_expert"   : True,
            }

        response=client.post('/users/sign-up',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message" : "INVALID_PASSWORD"
        })
    
    def test_signup_post_invalid_nickname(self):
        client     = Client()
        test_data = {
            "email"       : "test001@gmail.com",
            "password"    : "12345678",         
            "password"    : "testpassword",         
            "nickname"    : "testnickname",
            "is_expert"   : True,
            }

        response=client.post('/users/sign-up',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "NICKNAME_ALREADY_EXISTS"
        })

class LogInViewTest(TestCase):
    def setUp(self):
        hashed_password  = bcrypt.hashpw("testpassword12".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        User.objects.create(
            email        = "testemail@test.com",
            password     = hashed_password,
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_login_post_success(self):
        client           = Client()
        password         = "testpassword12"
        hashed_password  = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        test_data        = {
            "email"       : "testemail@test.com",
            "password"    : "testpassword12",
        }
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            response=client.post('/users/log-in',json.dumps(test_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_email(self):
        client     = Client()
        test_data = {
            "email"       : "testemailcom",
            "password"    : "testpassword12",
            "nickname"    : "testnickname",
            "is_expert"   : True,
        }
        response=client.post('/users/log-in',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{"message" : "INVALID_USER"})

    def test_login_post_invalid_password(self):
        client     = Client()
        test_data = {
            "email"       : "testemail12@test.com",
            "password"    : "test",         
            "nickname"    : "testnickname12",
            "is_expert"   : True,
            }

        response=client.post('/users/log-in',json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{"message" : "INVALID_USER"})
