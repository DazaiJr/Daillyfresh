from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home_redirect'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path("__reload__/", include("django_browser_reload.urls")),
]