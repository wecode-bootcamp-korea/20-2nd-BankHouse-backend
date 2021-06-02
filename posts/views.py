import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q, F
from django.db.models      import Count

from posts.models          import Post, LivingType, Space, Size, Style, Image
from users.models          import User

class PostsDetailView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({'message':'INVALID_POST'}, status=404)

        post = Post.objects.get(id = post_id)
        results = {
            'id'            : post.id,
            'size'          : post.size.name,
            'posted_time'   : post.created_at,
            'imgURL'        : post.image_set.first().image_url,
            'liked'         : post.like_set.count(), 
            'liked_nickname': [like.user.userinformation_set.first().nickname for like in post.like_set.all()]
        }

        return JsonResponse({'results':results}, status=200)
        