from django.urls import path

from user.views import UserCreateView, ProfileView, MyChallengeView

urlpatterns = [
    path("", UserCreateView.as_view(), name="user_creator"),
    path("profile/", ProfileView.as_view()),
    path("profile/my_challenges/", MyChallengeView.as_view()),
]
