from django.urls import path

from posts.views import PostsDetailView

urlpatterns = [
	path('/<int:post_id>', PostsDetailView.as_view()),
]
