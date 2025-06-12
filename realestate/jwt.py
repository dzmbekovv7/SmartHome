import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # no Authorization header

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None

            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user = User.objects.get(pk=payload['userId'])  # assuming token has 'userId'

            if user.is_blocked:
                raise exceptions.AuthenticationFailed('Ваш аккаунт был заблокирован.')

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Срок действия токена истёк.')

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Неверный токен.')

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь не найден.')
