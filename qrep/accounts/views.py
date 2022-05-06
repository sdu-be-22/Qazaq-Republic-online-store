from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . import forms
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile


def index(request):
    current_user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=current_user)
    context = dict()
    context['profile'] = profile
    print(current_user)
    print(profile.address, 'address jok')
    return render(request, 'user/user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user = request.user
            user_profile, _ = UserProfile.objects.get_or_create(user=user)

            if profile_form.cleaned_data.get('phone'):
                user_profile.phone = profile_form.cleaned_data.get('phone')
            if profile_form.cleaned_data.get('country'):
                user_profile.country = profile_form.cleaned_data.get('country')
            if profile_form.cleaned_data.get('image'):
                user_profile.image = profile_form.cleaned_data.get('image')
            if profile_form.cleaned_data.get('city'):
                user_profile.city = profile_form.cleaned_data.get('city')
            if profile_form.cleaned_data.get('address'):
                user_profile.address = profile_form.cleaned_data.get('address')

            user_profile.save()

            user_form.save()
            # profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)
        #     instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        form = forms.ProfileForm(instance=request.user)
    return render(request, 'user/user_update.html', context)
