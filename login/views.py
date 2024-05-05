from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from application.models import CustomUser

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Неудачная попытка входа
            messages.error(request, 'Неверный email или пароль.')
    return render(request, 'login/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Проверка совпадения паролей
        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        # Проверка уникальности email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже зарегистрирован.')
            return redirect('register')

        # Создание нового пользователя
        user = CustomUser.objects.create_user(email=email, password=password)
        user.save()

        # Автоматический вход после регистрации
        login(request, user)

        # Редирект на главную страницу
        return redirect('home')  # Замените 'home' на имя вашего URL-шаблона для главной страницы

    return render(request, 'login/register.html')

def logout_view(request):
    logout(request)
    # После выхода пользователя перенаправляем его на главную страницу или другую страницу, где требуется.
    return redirect('login') 