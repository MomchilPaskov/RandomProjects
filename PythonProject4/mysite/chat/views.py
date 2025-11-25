from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Chat, Message

@login_required
def chat_list(request):
    users=User.objects.exclude(id=request.user.id)
    return render(request, "chat/chat_list.html", {"users": users})

@login_required
def chat_room(request, user_id):
    other_user = User.objects.get(id=user_id)

    #Има ли някакъв чат
    chat = Chat.objects.filter(
        user1=request.user, user2=other_user
    ).first() or Chat.objects.filter(
        user1=other_user, user2=request.user
    ).first()

    # Ако чат не съществува, да го създаде
    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=other_user)

    messages = Message.objects.filter(chat=chat).order_by("timestamp")

    if request.method == "POST":
        content = request.POST.get("content")
        if content.strip():
            Message.objects.create(chat=chat, sender=request.user,content=content)
        return redirect("chat_room", user_id=other_user.id)

    return render(request, "chat/chat_room.html" , {
        "chat": chat,
        "messages": messages,
        "other_user": other_user
    })

@login_required
def chat_widget(request, user_id):
    other_user = User.objects.get(id=user_id)

    chat=Chat.objects.filter(
        user1=request.user, user2=other_user
    ).first() or Chat.objects.filter(
        user1=other_user, user2=request.user
    ).first()

    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=other_user)

    messages = Message.objects.filter(chat=chat).order_by("timestamp")

    return render(request, "partials/chat_messages.html", {
        "messages": messages,
        "user": request.user
    })

from django.http import JsonResponse

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(chat=chat, sender=request.user, content=content)
            return JsonResponse({
                'status': 'ok',
                'message': message.content,
                'sender': request.user.username,
                'timestamp': message.timestamp.strftime("%H:%M")
            })
    return JsonResponse({'status': 'error'})

@login_required
def chat_users(request):
    """Return all other users to show in chat list"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat/chat_users.html", {"users": users})
