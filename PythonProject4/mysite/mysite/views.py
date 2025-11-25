from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    other_users = None

    if request.user.is_authenticated:
        other_users = User.objects.exclude(id=request.user.id)

    return render(request, "home.html", {
        "other_users": other_users
    })
