from django.urls import path
from .views import HomePageView, TutoringPreviewPageView, TutoringsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page-view"),
    path("tutorings/", TutoringsPageView.as_view(), name="tutorings-page-view"),
    path("tutorings/<int:tutoring_id>/preview/", TutoringPreviewPageView.as_view(), name="tutoring-preview-page-view"),
]