import json
from json.decoder           import JSONDecodeError

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q, F
from django.db.models      import Count

from posts.models          import Post, LivingType, Space, Size, Style, Image, Comment
from users.models          import User
from util.utils            import login_required


class PostDetailView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({'message':'INVALID_POST'}, status=404)

        post = Post.objects.get(id = post_id)
        results = {
            'id'            : post.id,
            'size'          : post.size.name,
            'posted_time'   : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'imgURL'        : post.image_set.first().image_url,
            'liked'         : post.like_set.count(), 
            'liked_nickname': [like.user.userinformation_set.first().nickname for like in post.like_set.all()]
        }

        return JsonResponse({'results':results}, status=200)

class CommentView(View):
    @login_required
    def post(self, request):
        try :
            data        = json.loads(request.body)
            content     = data['content']
            post_id     = data['post_id']
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
        
class PostView(View):
    def get(self, request):
        orderby     = request.GET.get('orderby', 'hit')
        livingtype  = request.GET.get('livingtype', None)
        space       = request.GET.get('space', None)
        size        = request.GET.get('size', None)
        style       = request.GET.get('style', None)
        expert      = request.GET.get('expert', None)
        offset      = int(request.GET.get('offset', 1))
        limit       = int(request.GET.get('limit', 16))
        
        q     = Q()
        start = (offset-1) * limit
        end   = offset * limit

        order_by_data  = {'recent' : '-created_at', 'hit' : '-hit', 'like':'-likes'}
      
        if livingtype:
            q.add(Q(living_type__id = livingtype), q.OR)

        if space:
            q.add(Q(space__id = space), q.AND)

        if size:
            q.add(Q(size_id = size), q.AND)
        
        if style:
            q.add(Q(style__id = style), q.AND)

        if expert:
            q.add(Q(user__userinformation__is_expert = expert), q.AND)


        results = [{
                'post_id'                  : post.id,
                'description'              : post.description,
                'hit'                      : post.hit,
                'post_image'               : post.image_set.first().image_url 
                                            if post.image_set.filter().exists() else '',
                'like_count'               : post.likes,
                'comment_count'            : post.comment_set.count(),
                'recently_comment'         : post.comment_set.first().content
                                            if post.comment_set.filter().exists() else '',
                'recently_comment_nickname': post.comment_set.first().user.userinformation_set.first().nickname
                                           if post.comment_set.filter().exists() else '',
                'recently_comment_image'   : post.comment_set.first().user.userinformation_set.first().image_url
                                           if post.comment_set.filter().exists() else '',  
                'user_nickname'            : post.user.userinformation_set.first().nickname,
                'user_image'               : post.user.userinformation_set.first().image_url,
                } for post in Post.objects.filter(q).annotate(likes = Count('like__id')).order_by(order_by_data[orderby])
            ]
            
        return JsonResponse({'results': results[start: end], 'post_count': len(results)}, status = 200)
