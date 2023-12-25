from django.urls import path

from user.views import UserCreateView

urlpatterns = [
    path("", UserCreateView.as_view()),
    # path('/<str:name>', UserView.as_view()),
]
