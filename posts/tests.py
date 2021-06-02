import json

from django.test  import TestCase, Client

from posts.models import Post, LivingType, Space, Size, Style, Image, Like
from users.models import User, UserInformation

class PostsTest(TestCase):
    def setUp(self):
        client = Client()

        #livingtype
        LivingType.objects.create(
                id    = 1,
                name  = '원룸&오피스텔',
            )

        LivingType.objects.create(
                id    = 2,
                name  = '아파트',
            )
        
        LivingType.objects.create(
                id    = 3,
                name  = '단독주택',
            )

        #space
        Space.objects.create(
            id = 1,
            name  = '서재',
        )
    
        Space.objects.create(
            id = 2,
            name  = '주방',
        )

        Space.objects.create(
            id = 3,
            name  = '발코니',
        )

        Space.objects.create(
            id = 4,
            name  = '화장실',
        )

        Space.objects.create(
            id = 5,
            name  = '거실',
        )

        #size
        Size.objects.create(
            id = 1,
            name  = '10평 미만',
        )

        Size.objects.create(
            id = 2,
            name  = '10평대',
        )

        Size.objects.create(
            id = 3,
            name  = '20평대',
        )

        Size.objects.create(
            id = 4,
            name  = '30평대',
        )

        Size.objects.create(
            id = 5,
            name  = '40평대',
        )

        Size.objects.create(
            id = 6,
            name  = '50평대 이상',
        )

        #style
        Style.objects.create(
            id = 1,
            name  = '모던',
        )

        Style.objects.create(
            id = 2,
            name  = '북유럽',
        )

        Style.objects.create(
            id = 3,
            name  = '내추럴',
        )
        
        #user
        User.objects.create(
            id               = 1,
            email            = 'eiali@naver.com',
            password         = 'flaiw2913',
            kakao_id         = False,
        )

        User.objects.create(
            id               = 2,
            email            = 'uejcor@naver.com',
            password         = 'dnjel9234',
            kakao_id         = False,
        )

        User.objects.create(
            id               = 3,
            email            = 'alewf@naf.com',
            password         = 'fnke9244',
            kakao_id         = True,
        )

        User.objects.create(
            id               = 4,
            email            = 'eiali@naver.com',
            password         = 'girizlek682',
            kakao_id         = True,
        )

        User.objects.create(
            id               = 5,
            email            = 'lkejfk@email.com',
            password         = 'vmdkwoi728',
            kakao_id         = False,
        )
        
        User.objects.create(
            id               = 6,
            email            = 'mviei@mail.com',
            password         = 'nfksuiej6739',
            kakao_id         = True,
        )

        User.objects.create(
            id               = 7,
            email            = 'onejc@daum.com',
            password         = 'pqjdjvj837',
            kakao_id         = False,
        )

        User.objects.create(
            id               = 8,
            email            = 'llfj@naver.com',
            password         = 'yerkfmbo375',
            kakao_id         = False,
        )

        User.objects.create(
            id               = 9,
            email            = 'pejck@naver.com',
            password         = 'ejjjal6556',
            kakao_id         = True,
        )

        #user_information
        UserInformation.objects.create(
            id        = 1,
            nickname  = '나나',
            is_expert = True,
            user      = User.objects.get(id = 1)
        )

        UserInformation.objects.create(
            id        = 2,
            nickname  = '모모',
            is_expert = False,
            user      = User.objects.get(id = 2)
        )

        UserInformation.objects.create(
            id        = 3,
            nickname  = '누누',
            is_expert = False,
            user      = User.objects.get(id = 3)
        )

        UserInformation.objects.create(
            id        = 4,
            nickname  = '니니',
            is_expert = True,
            user      = User.objects.get(id = 4)
        )

        UserInformation.objects.create(
            id        = 5,
            nickname  = '다다',
            is_expert = False,
            user      = User.objects.get(id = 5)
        )

        UserInformation.objects.create(
            id        = 6,
            nickname  = '가가',
            is_expert = True,
            user      = User.objects.get(id = 6)
        )

        UserInformation.objects.create(
            id        = 7,
            nickname  = '바바',
            is_expert = True,
            user      = User.objects.get(id = 7)
        )

        UserInformation.objects.create(
            id        = 8,
            nickname  = '아아',
            is_expert = False,
            user      = User.objects.get(id = 8)
        )

        UserInformation.objects.create(
            id        = 9,
            nickname  = '하하',
            is_expert = False,
            user      = User.objects.get(id = 9)
        )


        #post
        Post.objects.create(
            id          = 73,
            description = '',
            hit         = 44,
            living_type = LivingType.objects.get(id = 2),
            size        = Size.objects.get(id = 1),
            space       = Space.objects.get(id = 5),
            style       = Style.objects.get(id = 1),
            user        = User.objects.get(id = 7),
        )

        Post.objects.create(
            id          = 76,
            description = '',
            hit         = 4647,
            living_type = LivingType.objects.get(id = 2),
            size        = Size.objects.get(id = 1),
            space       = Space.objects.get(id = 5),
            style       = Style.objects.get(id = 1),
            user        = User.objects.get(id = 7),
        )

        Post.objects.create(
            id          = 3,
            description = '',
            hit         = 23,
            living_type = LivingType.objects.get(id = 2),
            size        = Size.objects.get(id = 1),
            space       = Space.objects.get(id = 5),
            style       = Style.objects.get(id = 2),
            user        = User.objects.get(id = 7),
        )

        #image
        Image.objects.create(
            image_url = "https://images.unsplash.com/photo-1543248939-ff40856f65d4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MzJ8fHBob3RvJTIwZnJhbWV8ZW58MHx8MHx8&auto=format&fit=crop&w=900&q=60",
            post      = Post.objects.get(id = 73),
        )

        Image.objects.create(
            image_url = "https://images.unsplash.com/photo-1565031491910-e57fac031c41?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Njh8fHRhYmxlfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            post      = Post.objects.get(id = 3),
        )

        #like
        Like.objects.create(
            post = Post.objects.get(id = 73),
            user = User.objects.get(id = 4),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 1),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 2),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 3),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 4),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 5),
        )

        Like.objects.create(
            post = Post.objects.get(id = 3),
            user = User.objects.get(id = 6),
        )

    def tearDown(self):
        LivingType.objects.all().delete()
        Size.objects.all().delete()
        Space.objects.all().delete()
        Style.objects.all().delete()
        UserInformation.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()
        Image.objects.all().delete()

    def test_posts_detail_get_success(self):
        client   = Client()
        response = client.get('/posts/3')
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(response.json(),
            {
                "results": {
                    "id": 3,
                    "imgURL": "https://images.unsplash.com/photo-1565031491910-e57fac031c41?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Njh8fHRhYmxlfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
                    "liked": 6,
                    "liked_nickname": [
                        "나나",
                        "모모",
                        "누누",
                        "니니",
                        "다다",
                        "가가"
                    ],
                    "posted_time": "2021-06-02T02:30:03.407Z",
                    "size": "10평 미만"
                }
            }
        )
        self.assertEqual(response.status_code, 200)
