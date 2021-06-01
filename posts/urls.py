from django.urls import path

urlpatterns = [
    path("comments", CommentView.as_view()),
    ]