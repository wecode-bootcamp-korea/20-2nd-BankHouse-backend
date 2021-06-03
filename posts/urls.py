from django.urls import path

from posts.views import PostView, PostDetailView, CommentView

urlpatterns = [
	path('', PostView.as_view()),
	path('/<int:post_id>', PostDetailView.as_view()),
	path('/post', PostDetailView.as_view()),
    path("/comments", CommentView.as_view()),
    path("/comments/<int:post_id>", CommentView.as_view()),
]
