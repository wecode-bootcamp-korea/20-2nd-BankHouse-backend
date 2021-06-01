from django.urls import path
from posts.views import CommentPostView, CommentGetView

urlpatterns = [
    path("/comments", CommentPostView.as_view()),
    path("/comments/<int:post_id>", CommentGetView.as_view()),
    ]