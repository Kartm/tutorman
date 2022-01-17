from django.urls import path
from .views import HomePageView, TutoringParticipatePageView, TutoringsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page-view"),
    path("tutorings/", TutoringsPageView.as_view(), name="tutorings-page-view"),
    path("tutorings/<int:tutoring_id>/participant/<int:participant_id>", TutoringParticipatePageView.as_view(), name="tutoring-participate-page-view"),
]