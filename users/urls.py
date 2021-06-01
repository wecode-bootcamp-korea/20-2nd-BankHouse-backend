from django.urls     import path
from users.views     import SignUpView, LogInView, KakaoLogInView

urlpatterns = [
    path("/sign-up", SignUpView.as_view()),
    path("/log-in", LogInView.as_view()),
    path("/log-in/kakao", KakaoLogInView.as_view()),
    ]
