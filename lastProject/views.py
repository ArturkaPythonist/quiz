# views.py

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .forms import ProfileForm
from .models import User

class home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

class profile(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html', {})

class quiz(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz.html', {})

class login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})

class register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {})

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        email = request.POST.get('email')

        # Проверка, что пароли совпадают
        if password != password_repeat:
            error = 'Пароли не совпадают'
            return render(request, 'register.html', {'error': error})

        # Проверка наличия пользователя с таким именем
        if User.objects.filter(username=username).exists():
            error = 'Пользователь с таким именем уже существует'
            return render(request, 'register.html', {'error': error})
        else:
            # Создание нового пользователя с захешированным паролем
            user = User.objects.create(username=username, email=email)
            user.set_password(password)  # Хешируем пароль
            user.save()
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):git init
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Попытка аутентификации пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # используем auth_login вместо login
            request.session['user_id'] = user.id
            # Аутентификация успешна, перенаправляем пользователя на домашнюю страницу
            return redirect('home')  # Замените 'home' на имя вашей домашней страницы
        else:
            # Аутентификация неудачна, выдаем сообщение об ошибке
            error = 'Неправильное имя пользователя или пароль'
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

class logout(LogoutView):
    next_page = reverse_lazy('home')

def UserProfile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def Get_UserProfile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_profile = UserProfile.objects.get(id = user_id)
        print("12341")
        print(request.user)
        print(user_profile)
    return render(request, 'profile.html', {'user_profile': user_profile})