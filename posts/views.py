import json
from json.decoder   import JSONDecodeError

from django.http    import JsonResponse
from django.views   import View

from posts.models   import Post, Comment
from users.models   import User
from util.utils     import login_required


class CommentPostView(View):
    @login_required
    def post(self, request):
        try :
            data        = json.loads(request.body)
            content     = data['content']
            post_id     = str(data['post_id'])
            user        = request.user
            sub_comment = data.get('sub_comment_id', None)

            if not content and post_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({'message':"POST_DOES_NOT_EXIST"}, status=404)
            
            Comment.objects.create(
                content     = content,
                user        = user.id,
                post        = post_id,
                sub_comment = sub_comment
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class CommentGetView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({'message':'POST_DOES_NOT_EXIST'}, status=404)
 
        comments  = Comment.objects.filter(post=post_id)
        comment_data = [{
            "nickname"    : comment.user.userinformation_set.first().nickname,
            "img_url"     : comment.user.userinformation_set.first().image_url,
            "comment"     : comment.content if comment.sub_comment is None else "",
            "sub_comment" : comment.content if comment.sub_comment is not None else "",
            "date"        : comment.created_at,
            } for comment in comments]

        return JsonResponse({'data': comment_data}, status=200)