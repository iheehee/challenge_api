from django.urls import path

from user.views import UserCreateView, ProfileView

urlpatterns = [
    path("", UserCreateView.as_view()),
    path("profile/", ProfileView.as_view()),
]
