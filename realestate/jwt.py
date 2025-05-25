import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # no auth provided

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None

            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user = User.objects.get(pk=payload['userId'])  # assuming 'userId' in token
            return (user, token)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token')
