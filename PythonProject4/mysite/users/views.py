from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, login
from .models import Profile

from .forms import ProfileForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "users/profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {"form": form})

@login_required
def notifications(request):
    return render(request, "users/notifications.html")

@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile has been deleted.")
        return redirect("home")
    return render(request, "users/confirm_delete.html")

