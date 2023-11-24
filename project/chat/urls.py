from django.urls import path
from . import views

urlpatterns = [
    path('<int:chat_id>/message', views.Message.as_view())
]
