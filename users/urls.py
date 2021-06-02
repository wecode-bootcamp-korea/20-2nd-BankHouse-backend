from django.urls     import path
from users.views     import KakaoLogInView

urlpatterns = [
    path("/log-in/kakao", KakaoLogInView.as_view()),
]