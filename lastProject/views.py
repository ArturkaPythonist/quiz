# views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import UserProfileForm
from .models import UserProfile, User, Question, Choice
from django.http import JsonResponse
from random import sample


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


class check_answer(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'check_answer.html', {})


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


def user_login(request):
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


def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,
                               instance=user_profile)  # Обрабатываем также загруженные файлы
        if form.is_valid():
            user_profile = form.save(commit=False)
            # Получаем ссылку на сохраненное изображение и сохраняем ее в поле profile_picture_url
            user_profile.profile_picture_url = user_profile.profile_picture.url
            user_profile.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_profile_picture_url = ' profile_pics/69625e0cb05afcde2c8d3861e23853db.png'
        UserProfile.objects.create(user=instance, profile_picture=default_profile_picture_url)


@login_required
def start_quiz(request):
    # Получаем случайные 10 вопросов
    request.session['correct_answers'] = 0
    all_questions = list(Question.objects.all())
    selected_questions = sample(all_questions, min(len(all_questions), 11))  # Выбираем максимум 10 вопросов

    # Сохраняем ID выбранных вопросов в сессии
    request.session['selected_questions'] = [q.id for q in selected_questions]
    request.session['current_question_index'] = 1  # Начинаем с индекса 0 (первый вопрос)

    return JsonResponse({'message': 'Quiz started', 'first_question': 0, 'total_questions': len(selected_questions)})


@login_required
def get_question(request, question_index):
    selected_question_ids = request.session.get('selected_questions', [])

    try:
        question_id = selected_question_ids[question_index]
        question = get_object_or_404(Question, pk=question_id)
        choices = list(Choice.objects.filter(question=question))
        # Перемешиваем варианты ответов
        shuffled_choices = sample(choices, len(choices))
        choices_data = [{'id': choice.id, 'text': choice.choice_text, 'is_correct': choice.is_correct} for choice in
                        shuffled_choices]
        data = {
            'id': question.id,
            'text': question.question_text,
            'choices': choices_data
        }
        return JsonResponse(data)
    except IndexError:
        return JsonResponse({'error': 'Question index out of range'}, status=400)


@login_required
@csrf_exempt
@require_POST
def submit_answer(request):
    try:
        data = json.loads(request.body)
        choice_id = data.get('choice_id')
        choice = get_object_or_404(Choice, pk=choice_id)

        if choice.is_correct:
            correct_answers = request.session.get('correct_answers', 0) + 1
            request.session['correct_answers'] = correct_answers
        else:
            correct_answers = request.session.get('correct_answers', 0)

        # Обновляем текущий индекс вопроса в сессии
        current_question_index = request.session.get('current_question_index', 0)
        current_question_index += 1
        request.session['current_question_index'] = current_question_index

        selected_questions = request.session.get('selected_questions', [])
        total_questions = len(selected_questions)

        if current_question_index < total_questions:
            return JsonResponse({
                'message': 'Answer submitted successfully',
                'next_question_index': current_question_index,
                'correct_answers': correct_answers,
                'total_questions': total_questions
            })
        else:
            return JsonResponse({
                'message': 'Quiz finished',
                'correct_answers': correct_answers,
                'total_questions': total_questions
            })
    except (KeyError, ValueError) as e:
        return JsonResponse({'error': f'Invalid data provided: {str(e)}'}, status=400)
