from django.contrib import admin
from django.urls import path, include
from core.views import home, signup_view, login_view, logout_view, cart_page, add_address, place_order
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home_redirect'),
    
    # Auth URLs
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Cart & Checkout URLs
    path('cart/', cart_page, name='cart_page'),
    path('add-address/', add_address, name='add_address'),
    path('place-order/', place_order, name='place_order'),
    
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)