from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home_redirect'),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )