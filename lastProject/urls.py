from django.urls import path
from .views import home, quiz, login, register, user_register, user_login, logout, user_profile, check_answer, \
    get_question, start_quiz, submit_answer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', home.as_view(), name='home'),
                  path('login/', login.as_view(), name='login'),
                  path('user_login/', user_login, name='user_login'),
                  path('register/', register.as_view(), name='register'),
                  path('user_register/', user_register, name='user_register'),
                  path('profile/', user_profile, name='user_profile'),
                  path('logout/', logout.as_view(), name='logout'),
                  path('quiz/', quiz.as_view(), name='quiz'),
                  path('quiz/start/', start_quiz, name='start_quiz'),
                  path('quiz/question/<int:question_index>/', get_question, name='get_question'),
                  path('quiz/submit/', submit_answer, name='submit_answer'),
                  path('quiz/check_answer/', check_answer.as_view(), name='check_answer')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
