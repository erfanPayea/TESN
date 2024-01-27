from django.urls import path
from . import views

urlpatterns = [
    path('<int:chat_id>/message', views.Message.as_view()),
    path('<int:chat_id>', views.Chat.as_view()),
    path('', views.Chat.as_view())
]
