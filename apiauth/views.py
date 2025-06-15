from django.core.exceptions import ObjectDoesNotExist
from .serializers import RegisterSerializer, UpdateProfileSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
import logging
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import random
logger = logging.getLogger(__name__)
from rest_framework.views import exception_handler
import matplotlib.pyplot as plt
from io import BytesIO
from houses.models import House
import seaborn as sns
import base64
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
import io
from houses.models import Comment
def generate_confirmation_code():
    return ''.join(random.choices('0123456789', k=6))
def send_confirmation_email(user, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Здравствуйте, {user.username}! Подтвердите вашу почту с помощью следующего кода: {confirmation_code}'
    from_email = 'SmartHome <aziretdzumabekov19@gmail.com>'
    recipient_list = [user.email]

    html_message = f'''
    <html>
        <head>
            <style>
                body {{
                    background-color: #f2f4f6;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h2 {{
                    color: #333333;
                }}
                .content p {{
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.6;
                }}
                .code {{
                    margin: 20px auto;
                    font-size: 28px;
                    font-weight: bold;
                    background-color: #e0f7e9;
                    color: #2e7d32;
                    padding: 15px;
                    text-align: center;
                    border-radius: 5px;
                    width: 200px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #999999;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Подтверждение регистрации</h2>
                </div>
                <div class="content">
                    <p>Здравствуйте, <strong>{user.username}</strong>!</p>
                    <p>Спасибо за регистрацию на SmartHome.</p>
                    <p>Пожалуйста, используйте следующий код для подтверждения вашей почты:</p>
                    <div class="code">{confirmation_code}</div>
                    <p>Если вы не регистрировались, просто проигнорируйте это письмо.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 SmartHome. Все права защищены.</p>
                </div>
            </div>
        </body>
    </html>
    '''

    try:
        print(user.email)
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    except Exception as e:
        logger.error(f"Ошибка отправки письма подтверждения: {str(e)}")
def send_password_reset_email(user, reset_code):
    subject = 'Сброс пароля'
    message = f'Здравствуйте, {user.username}! Ваш код для сброса пароля: {reset_code}'
    from_email = 'ExchangeWork <aziretdzumabekov19@gmail.com>'
    recipient_list = [user.email]

    html_message = f'''
    <html>
        <head>
            <style>
                body {{
                    background-color: #f2f4f6;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h2 {{
                    color: #333333;
                }}
                .content p {{
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.6;
                }}
                .code {{
                    margin: 20px auto;
                    font-size: 28px;
                    font-weight: bold;
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 15px;
                    text-align: center;
                    border-radius: 5px;
                    width: 200px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #999999;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Сброс пароля</h2>
                </div>
                <div class="content">
                    <p>Здравствуйте, <strong>{user.username}</strong>!</p>
                    <p>Мы получили запрос на сброс вашего пароля.</p>
                    <p>Пожалуйста, введите следующий код для создания нового пароля:</p>
                    <div class="code">{reset_code}</div>
                    <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 ExchangeWork. Все права защищены.</p>
                </div>
            </div>
        </body>
    </html>
    '''


    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


@csrf_exempt
def consultation_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            city = data.get('city')
            phone = data.get('phone')
            message = data.get('message')

            if not all([name, city, phone, message]):
                return JsonResponse({'error': 'Все поля обязательны'}, status=400)

            subject = f'Новая заявка на консультацию от {name}'
            body = f'Имя: {name}\nГород: {city}\nТелефон: {phone}\nСообщение:\n{message}'

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # отправляем на сам email
                fail_silently=False,
            )
            return JsonResponse({'success': 'Заявка успешно отправлена'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

class AdminStatsAPIView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        total_agents = User.objects.filter(is_agent=True).count()
        total_houses = House.objects.count()

        return Response({
            "total_users": total_users,
            "total_agents": total_agents,
            "total_houses": total_houses,
        })
# class AllGraphsAPIView(APIView):
#     def get_base64_img(self, fig):
#         buf = BytesIO()
#         fig.savefig(buf, format='png', bbox_inches='tight')
#         plt.close(fig)  # очень важно для освобождения памяти
#         buf.seek(0)
#         return base64.b64encode(buf.getvalue()).decode()
#
#     def get(self, request):
#         try:
#             # Только нужные поля
#             houses_data = list(House.objects.values('square', 'price', 'rooms', 'has_pool', 'location'))
#
#             # ----------- График 1: Площадь vs Цена -----------
#             square_price = [(h['square'], h['price']) for h in houses_data if h['square'] and h['price']]
#             x = [s for s, _ in square_price]
#             y = [p for _, p in square_price]
#             fig1 = plt.figure(figsize=(8, 5))
#             sns.scatterplot(x=x, y=y, alpha=0.6)
#             plt.title("Площадь дома vs Цена")
#             plt.xlabel("Площадь (м²)")
#             plt.ylabel("Цена")
#             plt.grid(True)
#             img1 = self.get_base64_img(fig1)
#
#             # ----------- График 2: Гистограмма комнат -----------
#             rooms = [h['rooms'] for h in houses_data if h['rooms'] is not None]
#             fig2 = plt.figure(figsize=(6, 4))
#             sns.histplot(rooms, bins=range(min(rooms), max(rooms)+2), discrete=True)
#             plt.title("Распределение количества комнат")
#             plt.xlabel("Количество комнат")
#             plt.ylabel("Частота")
#             plt.grid(axis='y')
#             img2 = self.get_base64_img(fig2)
#
#             # ----------- График 3: Пирог с бассейнами -----------
#             total = len(houses_data)
#             with_pool = sum(1 for h in houses_data if h['has_pool'])
#             without_pool = total - with_pool
#             fig3 = plt.figure(figsize=(6, 6))
#             plt.pie(
#                 [with_pool, without_pool],
#                 labels=['С бассейном', 'Без бассейна'],
#                 autopct='%1.1f%%',
#                 startangle=140,
#                 colors=['#66b3ff', '#ff9999']
#             )
#             plt.title("Дома с бассейном и без")
#             img3 = self.get_base64_img(fig3)
#
#             # ----------- График 4: Топ 10 локаций -----------
#             # Делается отдельно, напрямую через ORM
#             top_locations = (
#                 House.objects.values('location')
#                 .annotate(count=Count('id'))
#                 .order_by('-count')[:10]
#             )
#             locs = [l['location'] for l in top_locations]
#             counts = [l['count'] for l in top_locations]
#             fig4 = plt.figure(figsize=(10, 6))
#             sns.barplot(x=counts, y=locs, palette='viridis')
#             plt.title("Топ 10 локаций по количеству домов")
#             plt.xlabel("Количество домов")
#             plt.ylabel("Локация")
#             plt.tight_layout()
#             img4 = self.get_base64_img(fig4)
#
#             return Response({
#                 "charts": [
#                     {"title": "Площадь дома vs Цена", "image": img1},
#                     {"title": "Распределение количества комнат", "image": img2},
#                     {"title": "Дома с бассейном и без", "image": img3},
#                     {"title": "Топ 10 локаций по количеству домов", "image": img4},
#                 ]
#             })
#
#         except MemoryError:
#             return Response({"error": "Недостаточно памяти для генерации графиков"}, status=500)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

class IsAdminOrAgent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.is_agent))

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrAgent]

    def get(self, request):
        users = User.objects.all()
        data = []
        for u in users:
            data.append({
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_actively_looking": u.is_actively_looking,
                "is_agent": u.is_agent,
                "is_superuser": u.is_superuser,
                "is_blocked": u.is_blocked,
            })
        return Response(data, status=status.HTTP_200_OK)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)
def block_user_tokens(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        try:
            BlacklistedToken.objects.get_or_create(token=token)
        except Exception:
            pass
class BlockUserView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, user_id):
        try:
            user_to_block = User.objects.get(id=user_id)
            block_user_tokens(user_to_block)
            user_to_block.is_blocked = True
            user_to_block.save()
            return Response({'detail': 'User blocked and tokens blacklisted.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    user = context['request'].user if context.get('request') else None
    if user and user.is_authenticated and user.is_blocked:
        return Response({"detail": "Ваш аккаунт был заблокирован."}, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, (InvalidToken, TokenError)):
        return Response({"detail": "Токен истёк или недействителен. Войдите заново."}, status=status.HTTP_401_UNAUTHORIZED)

    return response

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if getattr(user, 'is_blocked', False):
            return Response(
                {"detail": "Ваш аккаунт был заблокирован."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": user.avatar.url if getattr(user, 'avatar', None) else None,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at,
                "is_agent": getattr(user, 'is_agent', False),
                "is_blocked": user.is_blocked,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("CheckAuthView error: %s", str(e))
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            confirmation_code = generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()

            send_confirmation_email(user, confirmation_code)

            return Response({'message': 'User registered, please confirm your email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)


            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "Authentication successful",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": access_token,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
            except TokenError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            reset_code = generate_confirmation_code()  # Генерируем код сброса
            user.reset_code = reset_code
            user.save()

            send_password_reset_email(user, reset_code)  # Отправляем код на почту

            return Response({"message": "Password reset code sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User with this email not found."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reset_code = request.data.get('reset_code')

        if not reset_code:
            return Response({"message": "Reset code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(reset_code=reset_code)

            return Response({"message": "Code is valid, you can now reset your password."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Invalid reset code."}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Получаем новый пароль и его подтверждение
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Проверяем, что оба пароля введены
        if not new_password or not confirm_password:
            return Response({"message": "New password and confirmation are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пароли совпадают
        if new_password != confirm_password:
            return Response({"message": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем код сброса из запроса
        reset_code = request.data.get('reset_code')

        if not reset_code:
            return Response({"message": "Reset code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ищем пользователя с этим кодом сброса
            user = User.objects.get(reset_code=reset_code)

            # Обновляем пароль
            user.set_password(new_password)
            user.reset_code = None  # Очищаем код сброса после использования
            user.save()  # Сохраняем изменения в базе данных

            return Response({"message": "Password has been successfully reset."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Invalid reset code."}, status=status.HTTP_400_BAD_REQUEST)

class ResendCode(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"message": "User with this email not found."}, status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()

        send_confirmation_email(user, confirmation_code)

        return Response({"message": "The code has been sent."}, status=status.HTTP_200_OK)

class ConfirmEmailAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        if not email or not confirmation_code:
            return Response({"message": "Email and confirmation code are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ищем пользователя по email
            user = User.objects.get(email=email)

            if str(user.confirmation_code).strip() == str(confirmation_code).strip():
                user.email_confirmed = True
                user.confirmation_code = None
                user.save()
                return Response({"message": "Your email has been confirmed! You can now log in."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)


        except User.DoesNotExist:
            return Response({"message": "User with this email not found."}, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)