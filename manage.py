#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import urllib.request
import subprocess
import shutil
from pytube import YouTube
from pydub import AudioSegment
from flask import Flask, request, jsonify
# import moviepy.editor as mp # type: ignore
import speech_recognition as sr

# from myProject import myApp

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def ensure_yt_dlp():
    """
    Ensure yt-dlp is installed. If not, install it.
    """
    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed. Installing...")
        subprocess.run(["pip", "install", "yt-dlp"], check=True)

def process_youtube_video(youtube_url, language="bn-BD", output_path="audio", chunk_length_ms=60000):
    try:
        # Ensure yt-dlp is installed
        ensure_yt_dlp()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Download audio using yt-dlp
        print("Downloading audio...")
        command = [
            "yt-dlp",
            "-f",
            "bestaudio[ext=m4a]",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "-o",
            f"{output_path}/audio.%(ext)s",
            youtube_url
        ]
        subprocess.run(command, check=True)

        audio_file = os.path.join(output_path, "audio.mp3")

        if not os.path.exists(audio_file):
            raise FileNotFoundError("Audio file could not be downloaded.")

        print(f"Audio downloaded to {audio_file}")

        # Split audio into chunks
        print("Splitting audio into chunks...")
        audio = AudioSegment.from_file(audio_file)
        chunks = []
        for start in range(0, len(audio), chunk_length_ms):
            chunk = audio[start:start + chunk_length_ms]
            chunk_filename = f"{output_path}/chunk_{start // chunk_length_ms}.wav"
            chunk.export(chunk_filename, format="wav")
            chunks.append(chunk_filename)

        # Transcribe each chunk
        print("Transcribing audio...")
        recognizer = sr.Recognizer()
        transcribed_text = ""

        for chunk in chunks:
            with sr.AudioFile(chunk) as source:
                audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                transcribed_text += text + "\n"
            except sr.UnknownValueError:
                transcribed_text += "[Unintelligible]\n"
            except sr.RequestError as e:
                transcribed_text += f"[Error: {e}]\n"

        # Clean up temporary files
        for chunk in chunks:
            os.remove(chunk)
        os.remove(audio_file)

        return transcribed_text

    except Exception as e:
        print(f"Error: {e}")
        raise



app = Flask(__name__)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    youtube_url = data.get("youtube_url")
    language = data.get("language", "bn-BD")

    if not youtube_url:
        return jsonify({"error": "YouTube URL is required."}), 400

    try:
        transcription = process_youtube_video(youtube_url, language)
        return jsonify({"transcription": transcription})
    except Exception as e:
        return jsonify({"error": str(e)}), 500






if (__name__) == '__main__':
    main()
    app.run(debug=True)
