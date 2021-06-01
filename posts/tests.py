import json
import jwt
import bcrypt

from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock

from posts.models   import Comment, Post
from users.models   import User, UserInformation
from util.utils     import login_required
from my_settings    import SECRET_KEY, ALGORITHM

class CommentPostViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            id      = 1,
            email   = "test123@test.com"
        )
        self.token = jwt.encode({'user_id' : User.objects.get(email = 'test123@test.com').id}, SECRET_KEY, algorithm = ALGORITHM)
    
    def tearDown(self):
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_comment_post_success(self):    
        client    = Client()
        test_data = {
            "content" : "test comments",
            "post_id" : "1",
        }
        header = {"HTTP_Authorization" : self.token}
        response=client.post('/posts/comments',json.dumps(test_data), **header, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "message": "SUCCESS",
        })
        
    def test_comment_post_key_error(self):
        client    = Client()
        test_data = {
            "user_id" : 1,
        }
        header = {"HTTP_Authorization" : self.token}
        response=client.post('/posts/comments',json.dumps(test_data), **header, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message" : "KEY_ERROR"
        })

    def test_comment_post_invalid_post(self):
        client    = Client()
        test_data = {
            "content" : "test comments",
            "post_id" : "1000",
        }
        header = {"HTTP_Authorization" : self.token}
        response=client.post('/posts/comments',json.dumps(test_data), **header, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{
            "message" : "POST_DOES_NOT_EXIST"
        })

class CommentGetViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            id      = 1,
            email   = "test123@test.com"
        )
    
    def tearDown(self):
        Comment.objects.all().delete()

    def test_comment_get_success(self):
        client           = Client()

        response=client.get('/posts/comments/1',json.dumps(test_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "message" : "SUCCESS"
        })
        
    def test_comment_get_fail_invalid_post(self):
        client    = Client()

        response=client.get('/posts/comments/1000',json.dumps(test_data), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{
            "message" : "POST_DOES_NOT_EXIST"
        })