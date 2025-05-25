from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import consumers
urlpatterns = [
    re_path(r'ws/online/(?P<user_id>\w+)/$', consumers.OnlineStatusConsumer.as_asgi()),
    path('admin/', admin.site.urls),
    path('', include('realestate.urls')),
    path('', include('apiauth.urls')),
    path('', include('houses.urls')),
    path('', include('chat.urls')),
    path('', include('agents.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)