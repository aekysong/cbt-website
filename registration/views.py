from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile


# Create your views here.

def signup(request):
    if request.method == "POST":
        try:
            if request.POST['password'] == request.POST['password_confirm']:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"])
                type = request.POST["type"]
                profile = Profile(user=user, type=type)
                if type != "professor" and type != "PRF":
                    profile.accept = True
                profile.save()
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, 'signup.html', {'error': '비밀번호를 확인해주세요'})
        except IntegrityError as e:
            return render(request, 'signup.html', {'error': '이미 있는 아이디입니다'})
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '아이디나 비밀번호가 맞지 않습니다'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
