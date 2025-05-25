from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Currency
from .serializers import CurrencySerializer
from .models import House, Comment, View
from .serializers import HouseSerializer, CommentSerializer, LikeSerializer,CurrencyAdminSerializer
from .permissions import IsOwnerOrReadOnly
import requests
from django.core.mail import send_mail
import random
from django.conf import settings
verification_codes = {}  # Лучше заменить на Redis в проде
from .models import EmailVerification
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
User = get_user_model()


class SendVerificationCode(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email обязателен'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=email, email=email)

        code = str(random.randint(100000, 999999))
        verification = EmailVerification.objects.create(user=user, code=code)

        send_mail(
            'Код подтверждения',
            f'Ваш код: {code}',
            'admin@site.com',
            [email],
        )
        return Response({'message': 'Код отправлен на почту'}, status=200)

class VerifyCode(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'error': 'Email и код обязательны'}, status=400)

        try:
            user =User.objects.get(email=email)
            verification = EmailVerification.objects.filter(
                user=user, code=code, is_verified=False
            ).latest('created_at')

            # Проверка срока действия — например, 10 минут
            if timezone.now() - verification.created_at > timedelta(minutes=10):
                return Response({'error': 'Код устарел'}, status=400)

            verification.is_verified = True
            verification.save()

            return Response({'verified': True})
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return Response({'verified': False}, status=400)

class ContactSeller(APIView):
    def post(self, request, house_id):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')

        try:
            house = House.objects.get(id=house_id)
        except House.DoesNotExist:
            return Response({'error': 'Объявление не найдено'}, status=404)

        seller_email = house.seller.email
        print(house.seller.email)
        send_mail(
            f"Сообщение от {name}",
            message,
            email,
            [seller_email],
        )
        return Response({'message': 'Сообщение отправлено продавцу'})
class CurrencyFetchFromAPI(APIView):
    permission_classes = [permissions.IsAdminUser]  # Только админ может вызывать

    def get(self, request):
        url = 'https://open.er-api.com/v6/latest/USD'  # Можно заменить на другой API
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('result') != 'success':
                return Response({'error': 'Не удалось получить данные с API'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            rates = data.get('rates', {})
            for code, rate in rates.items():
                Currency.objects.update_or_create(
                    code=code,
                    defaults={
                        'rate': rate,
                        'description': f"{code} currency"  # Можешь заменить на реальные описания
                    }
                )

            return Response({'message': 'Курсы успешно получены и сохранены в БД'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CurrencyListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)

class CurrencyAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencyAdminSerializer(currencies, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Используем бесплатный API для получения курсов валют
        url = 'https://open.er-api.com/v6/latest/USD'
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('result') != 'success':
                return Response({'error': 'Failed to fetch data from external API.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            rates = data.get('rates', {})
            for code, rate in rates.items():
                Currency.objects.update_or_create(
                    code=code,
                    defaults={'rate': rate}
                )
            return Response({'message': 'Currency rates updated successfully.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HouseListView(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.AllowAny]


class UnverifiedHousesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        houses = House.objects.filter(isVerified=False)
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data)


class VerifyHouseView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            house = House.objects.get(pk=pk)
            house.isVerified = True
            house.save()
            return Response({"message": "House verified"})
        except House.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

class RejectHouseView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            house = House.objects.get(pk=pk)
            house.delete()
            return Response({"message": "House deleted"})
        except House.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
class HouseDetailView(generics.RetrieveAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Only authenticated users are allowed to increase view count
        if request.user.is_authenticated:
            # Check if the user has already viewed this house
            already_viewed = View.objects.filter(house=instance, user=request.user).exists()

            if not already_viewed:
                View.objects.create(
                    house=instance,
                    user=request.user,
                    ip_address=self.get_client_ip()
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_client_ip(self):
        """Helper to get client IP address."""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
class HouseCreateView(generics.CreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class HouseUpdateView(generics.UpdateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class HouseDeleteView(generics.DestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        house_id = self.request.data.get('house')
        house = get_object_or_404(House, id=house_id)
        serializer.save(user=self.request.user, house=house)
class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'message': 'Комментарий удалён'}, status=status.HTTP_204_NO_CONTENT)

class HouseCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        house_id = self.kwargs.get('pk')
        return Comment.objects.filter(house_id=house_id).order_by('-created_at')

class LikeHouseToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        house = get_object_or_404(House, pk=pk)
        user = request.user

        if user in house.liked_by.all():
            house.liked_by.remove(user)
            liked = False
        else:
            house.liked_by.add(user)
            liked = True

        serializer = LikeSerializer({
            'house': house,
            'liked': liked,
            'like_count': house.like_count()
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
class LikeListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        house_id = self.kwargs.get('pk')
        house = get_object_or_404(House, pk=house_id)
        return house.liked_by.all()
