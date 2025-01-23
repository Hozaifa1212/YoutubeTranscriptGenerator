import os

import shutil
from pytube import YouTube
from moviepy.editor import AudioFileClip
import subprocess
from pytube import YouTube
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr


def ensure_yt_dlp():

    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed. Installing...")
        subprocess.run(["pip", "install", "yt-dlp"], check=True)

def download_audio(youtube_url, output_path="audio"):

    try:
        ensure_yt_dlp()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        print("Downloading audio using yt-dlp...")
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

        print(f"Downloaded audio to {audio_file}")
        return audio_file
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp command failed: {e}")
        raise
    except Exception as e:
        print(f"Error in audio download: {e}")
        raise


def split_audio(audio_file, chunk_length_ms=60000):

    try:
        audio = AudioSegment.from_file(audio_file)
        chunks = []
        for start in range(0, len(audio), chunk_length_ms):
            chunk = audio[start:start + chunk_length_ms]
            chunk_filename = f"chunk_{start // chunk_length_ms}.wav"
            chunk.export(chunk_filename, format="wav")
            chunks.append(chunk_filename)
        return chunks
    except Exception as e:
        print(f"Error splitting audio: {e}")
        raise

def transcribe_audio(audio_file, language="bn-BD"):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise