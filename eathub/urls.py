from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('api.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')), 
    path('api/v1/',include('api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
