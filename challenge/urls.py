from django.urls import path

from challenge.views import ChallengeView, ChallengeDetailView

urlpatterns = [
    path('', ChallengeView.as_view()),
    path('<int:pk>/', ChallengeDetailView.as_view()),
]
