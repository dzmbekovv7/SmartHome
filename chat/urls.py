from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', views.chat_view),
    path('chat-history/', views.get_chat_history ),
    path('chats/', views.list_chats),
    path('chats/create/', views.create_chat),
    path('chats/<int:chat_id>/messages/', views.get_chat_messages),
    path('chats/<int:chat_id>/send/', views.send_message),
    path('chats/<int:chat_id>/rename/', views.rename_chat),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
