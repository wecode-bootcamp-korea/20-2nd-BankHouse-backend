from django.urls import path

from posts.views import PostsDetailView, CommentView

urlpatterns = [
	path('/<int:post_id>', PostsDetailView.as_view()),
    path("/comments", CommentView.as_view()),
    path("/comments/<int:post_id>", CommentView.as_view()),
]
