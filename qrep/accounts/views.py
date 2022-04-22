from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import CreateUserForm
from .models import *


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('bastama:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Accounts was created for ' + user)
                return redirect('/accounts/login')
        # context = {'form':form}
        return render(request, 'accounts/register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('bastama:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('bastama:home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('bastama:home')
