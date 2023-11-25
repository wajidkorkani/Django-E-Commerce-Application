from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import Auth
import Core
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Auth.urls')),
    path('', include('Core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
