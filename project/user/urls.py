from django.urls import path
from . import views

urlpatterns = [
    path('', views.Users.as_view()),
    path('otp/', views.Users.as_view()),
    path('token/', views.Token.as_view()),
    path('following/', views.Following.as_view()),
    path('followers/', views.Followers.as_view())
]