from django.urls import path
from . import views
urlpatterns = [
    path('check/', views.CheckAuthView.as_view(), name='check-auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.UserLogOut.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('reset-password/', views.ResetPasswordAPI.as_view(), name='reset-password'),
    path('verify-email/', views.VerifyCodeAPI.as_view(), name='verify-email'),
    path('confirm-email/', views.ConfirmEmailAPI.as_view(), name='confirm-email'),
    path('resend-code/', views.ResendCode.as_view(), name='resend-code'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/block/<int:user_id>/', views.BlockUserView.as_view(), name='block-user'),
    path('graphs/all/', views.AllGraphsAPIView.as_view(), name='all-graphs'),
    path('consultation/', views.consultation_request, name='consultation_request'),
path("admin-stats/", views.AdminStatsAPIView.as_view(), name="admin-stats"),
    path('admin-dashboard/', views.all_graphs_api, name='market-trends-api'),

]
