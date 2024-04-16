from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("chat", include("chat.urls")),
    path("chat", TemplateView.as_view(template_name="home.html"), name="chat"),
    path("create_room/", TemplateView.as_view(template_name="newroom.html"), name="create_room"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="userlogin.html"), name="userlogin"),
    path('', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('create_room/createRoom', views.createRoom, name='createRoom'),
]
