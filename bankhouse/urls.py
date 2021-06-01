from django.urls import path, include

urlpatterns = [
    path("posts", include("posts.urls")),
    path("users", include("users.urls")),
]
