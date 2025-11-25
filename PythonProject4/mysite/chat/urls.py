from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('users/', views.chat_users, name='chat_users'),
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path("widget/<int:user_id>", views.chat_widget, name='chat_widget'),
    path('send-message/<int:chat_id>/', views.send_message, name='send_message'),
]