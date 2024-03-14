from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path("create_room/", TemplateView.as_view(template_name="newroom.html"), name="create_room"),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('newRoom', views.checkview, name='newRoom'),
    path('create_room/checkview', views.checkview, name='checkview'),
]