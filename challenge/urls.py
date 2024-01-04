from django.urls import path

from challenge.views import (
    ChallengeView,
    ChallengeDetailView,
    ChallengeCreateView,
    ChallengeApplyView,
    CertificatinoListView,
    CertificatinoCreateView,
    CertificatinoDetailView,
)

urlpatterns = [
    path("", ChallengeView.as_view()),
    path("create/", ChallengeCreateView.as_view()),
    path("<int:pk>/", ChallengeDetailView.as_view()),
    path("<int:pk>/apply/", ChallengeApplyView.as_view()),
    path("<int:pk>/certification/", CertificatinoListView.as_view()),
    path("<int:pk>/certification/create/", CertificatinoCreateView.as_view()),
    path(
        "<int:pk>/certification/<int:certification_id>/",
        CertificatinoDetailView.as_view(),
    ),
]
