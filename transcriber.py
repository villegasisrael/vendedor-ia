from google.cloud import speech
import os

# Configurar Google Cloud Speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-credentials.json"

def transcribe_audio(audio_path):
    """Convierte audio en texto"""
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="es-MX"
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript
