from django.urls import path
from .views import YouTubeTranscriptionView

urlpatterns = [
    path("transcribe/", YouTubeTranscriptionView.as_view(), name="youtube-transcribe"),
]
