from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.Users.as_view()),
    path('users/token/', views.Token.as_view()),
    path('users/follow/<int:user_id>', views.Follow.as_view())
]