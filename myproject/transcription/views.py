from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import download_audio, split_audio, transcribe_audio
import os

class YouTubeTranscriptionView(APIView):
    def post(self, request):
        video_url = request.data.get("video_url")

        if not video_url:
            return Response({"error": "YouTube URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Step 1: Download Audio
            audio_path = download_audio(video_url)

            print("Splitting audio into chunks...")
            chunks = split_audio(audio_path)

            transcribed_text = ""
            for chunk in chunks:
                print(f"Transcribing {chunk}...")
                text = transcribe_audio(chunk, language="bn-BD")
                transcribed_text += text + "\n"
            # Step 3: Delete Downloaded Audio File
            os.remove(audio_path)

            return Response({"transcribed_text": transcribed_text}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
