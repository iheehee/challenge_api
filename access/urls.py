from django.urls import path

from access.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
]
