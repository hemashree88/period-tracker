from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Period
import random
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'tracker/signup.html', {'error': 'Username and password are required.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'tracker/signup.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'tracker/signup.html')


TIPS = [
    "Drink plenty of water during your period 💧",
    "Try gentle yoga or stretching to ease cramps 🧘‍♀️",
    "Eat iron-rich foods like spinach and lentils 🌿",
    "Use a hot water bag to relieve pain 🔥",
    "Track your mood to notice hormonal patterns 😊",
    "Get enough sleep and rest during heavy flow days 😴",
    "Reduce caffeine to minimize bloating ☕",
]


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    periods = Period.objects.filter(user=request.user).order_by('-start_date')
    random_tip = random.choice(TIPS)
    return render(request, 'tracker/home.html', {'periods': periods, 'tip': random_tip})

@login_required
def add_period(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        mood = request.POST.get('mood')
        symptoms = request.POST.get('symptoms')
        Period.objects.create(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            mood=mood,
            symptoms=symptoms
        )
        return redirect('home')
    return render(request, 'tracker/add_period.html')
