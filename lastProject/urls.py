# urls.py
from django.urls import path
from .views import home, profile, quiz, login, register, user_register, user_login, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home.as_view(), name='home'),
    path ('login/', login.as_view(), name='login'),
    path('register/', register.as_view(), name='register'),
    path('user_register/', user_register, name='user_register'),
    path('user_login/', user_login, name='user_login'),
    path ('profile/', profile.as_view(), name='profile'),
    path('logout/', logout.as_view(), name='logout'),
    path('quiz/', quiz.as_view(), name='quiz'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)