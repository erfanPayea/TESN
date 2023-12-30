from django.urls import path
from . import views

urlpatterns = [
    path('post', views.Posts.as_view()),
    path('review', views.Reviews.as_view()),
    path('like', views.Likes.as_view()),
    path('all-user-posts/<int:user_id>', views.ViewAllPosts.as_view()),
    path('user-posts/<int:user_id>', views.ViewFirstSixPosts.as_view()),
    path('attraction-reviews/<int:attraction_id>', views.ViewFirstReview.as_view()),
    path('all-attraction-reviews/<int:attraction_id>', views.ViewAllReviews.as_view()),
]
