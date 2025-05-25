from django.urls import path
from .views import (
    HouseListView, HouseDetailView, HouseCreateView,
    HouseUpdateView, HouseDeleteView,
    CommentCreateView, HouseCommentListView,
    LikeHouseToggleView, LikeListView,
UnverifiedHousesView,
VerifyHouseView,
RejectHouseView,
CurrencyListView,
CurrencyAdminView,CurrencyFetchFromAPI,
CommentDeleteView,SendVerificationCode,VerifyCode,ContactSeller
)

urlpatterns = [
    path('send-code/', SendVerificationCode.as_view()),
    path('verify-code/', VerifyCode.as_view()),
    path('contact-seller/<int:house_id>/', ContactSeller.as_view()),
    path('houses/', HouseListView.as_view(), name='house-list'),
    path('houses/<int:pk>/', HouseDetailView.as_view(), name='house-detail'),
    path('houses/create/', HouseCreateView.as_view(), name='house-create'),
    path('houses/<int:pk>/update/', HouseUpdateView.as_view(), name='house-update'),
    path('houses/<int:pk>/delete/', HouseDeleteView.as_view(), name='house-delete'),

path('houses/unverified/', UnverifiedHousesView.as_view()),
path('houses/verify/<int:pk>/', VerifyHouseView.as_view()),
path('houses/reject/<int:pk>/', RejectHouseView.as_view()),
    # Comments
    path('houses/<int:pk>/comments/', HouseCommentListView.as_view(), name='house-comments'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Likes
    path('houses/<int:pk>/like/', LikeHouseToggleView.as_view(), name='house-like-toggle'),
    path('houses/<int:pk>/likes/', LikeListView.as_view(), name='house-like-list'),

    path('currencies/', CurrencyListView.as_view(), name='currency-list'),
    path('currency/admin/', CurrencyAdminView.as_view(), name='currency-admin'),
    path('currency/fetch/', CurrencyFetchFromAPI.as_view(), name='currency-fetch'),

]
