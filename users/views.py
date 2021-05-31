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
    
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except AttributeError:
            return JsonResponse({"message": "INVALID_USER"}, status=404)