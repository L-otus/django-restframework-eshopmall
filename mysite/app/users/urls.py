from django.urls import path
from app.users.views import loginview,coupounviews

urlpatterns = [
    path('login',loginview.as_view()),
    path('couponfind',coupounviews.as_view())
]