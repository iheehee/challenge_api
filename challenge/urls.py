from django.urls import path

from challenge.views import (
    ChallengeView,
    ChallengeDetailView,
    ChallengeCreateView,
    ChallengeApplyView,
)

urlpatterns = [
    path("", ChallengeView.as_view()),
    path("create/", ChallengeCreateView.as_view()),
    path("<int:pk>/", ChallengeDetailView.as_view()),
    path("<int:pk>/apply", ChallengeApplyView.as_view()),
]
