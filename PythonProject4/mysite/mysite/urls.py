from django.contrib import admin
from django.urls import path, include
from .views import home   # ✅ ADD THIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),   # ✅ USE THIS HOME
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
]
