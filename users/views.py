import json
import bcrypt
import jwt
import re
import requests

from django.views          import View
from django.http           import JsonResponse

from json.decoder          import JSONDecodeError

from users.models          import User, UserInformation
from my_settings           import SECRET_KEY, ALGORITHM


class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data["email"]
            nickname  = data["nickname"]
            password  = data.get("password", None)
            is_expert = data.get("is_expert", False)
            kakao_id  = data.get("kakao_id", None)

            email_validation    = re.compile('^[a-z0-9]+@[a-z0-9]+\.[a-z0-9.]+$', re.I)
            password_validation = re.compile('^(?=.*[a-z])(?=.*[0-9]).{8,}', re.I)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status=400)

            if UserInformation.objects.filter(nickname=nickname).exists():
                return JsonResponse({'message' : 'NICKNAME_ALREADY_EXISTS'}, status = 400)    

            if not email_validation.match(email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)
            
            if not password_validation.match(password) and password is not None:
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
                
            user = User.objects.create(
                email     = email,                
                password  = password if not password else hashed_password,
                kakao_id  = kakao_id,
                )
            UserInformation.objects.create(
                user_id   = user.id,
                nickname  = nickname,
                is_expert = is_expert,
                )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)  

class LogInView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user            = User.objects.get(email=data["email"])
            hashed_password = user.password.encode("utf-8")

            if not bcrypt.checkpw(data["password"].encode("utf-8"), hashed_password):
                return JsonResponse({"message":"INVALID_USER"}, status=401)

            access_token    = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({"message":"SUCCESS", "access_token": access_token}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except AttributeError:
            return JsonResponse({"message": "INVALID_USER"}, status=404)

class KakaoLogInView(View):
    def get(self, request):
        try:
            access_token     = request.headers.get('Authorization', None)
            headers          = {"Authorization" : f"Bearer {access_token}"}
            kakao_login_data = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers).json()

            if not kakao_login_data:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)
 
            if kakao_login_data.get('code') == -401:  
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)

            kakao_id      = str(kakao_login_data["id"])
            kakao_account = kakao_login_data["kakao_account"]
            email         = kakao_account["email"]

            if not User.objects.filter(email=email).exists() and email is not None:
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)

            login_token = jwt.encode({'user_id': kakao_id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'access_token' : login_token}, status=200)
    
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDecodeError"}, status=400)