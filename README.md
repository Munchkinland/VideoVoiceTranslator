# VideoVoiceTranslator
Using OpenAI  &amp; Google Text-to-Speech (gTTS)

Proyecto de Traducción de Videos
Este proyecto tiene como objetivo traducir el audio de un video desde el español al inglés y luego sincronizar el audio traducido con el video original. Utiliza varias librerías para la manipulación de audio y video, así como la API de OpenAI para la transcripción y traducción de texto.

Requisitos
Python 3.7+
Las siguientes librerías de Python:
moviepy
openai
gtts
tiktoken
pydub
python-dotenv
Para instalar estas librerías, puedes usar pip:

bash
Copiar código
pip install moviepy openai gtts tiktoken pydub python-dotenv
Un archivo .env con tu clave API de OpenAI:
makefile
Copiar código
OPENAI_API_KEY=tu_clave_api_aqui
Uso
El archivo principal del proyecto es main.py. Aquí está el flujo del programa:

Extraer audio del video:
Se extrae el audio del video y se guarda como un archivo WAV.
Dividir audio en segmentos:
El audio se divide en segmentos de 30 segundos para facilitar la transcripción.
Transcribir el audio:
Se utiliza la API de OpenAI para transcribir cada segmento de audio.
Traducir el texto transcrito:
Se traduce el texto transcrito del español al inglés utilizando la API de OpenAI.
Convertir texto traducido a voz:
Se utiliza gTTS para convertir el texto traducido a un archivo de audio en inglés.
Combinar el audio traducido con el video original:
Se sincroniza el nuevo audio con el video original y se guarda el video final.
Ejecución
Para ejecutar el script, asegúrate de tener un video en formato MP4 y modifica la variable video_path en el archivo main.py con la ruta de tu video. Luego, ejecuta:

bash
Copiar código
python main.py
Ejemplo de Código
python
Copiar código
import moviepy.editor as mp
import openai
from gtts import gTTS
import tiktoken
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def extraer_audio(video_path):
    try:
        video = mp.VideoFileClip(video_path)
        audio_path = "audio.wav"
        video.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error al extraer audio del video: {e}")
        return None

def dividir_audio(audio_path, segmento_duracion_ms=30000):
    audio = AudioSegment.from_wav(audio_path)
    duracion_total_ms = len(audio)
    segmentos = []

    for i in range(0, duracion_total_ms, segmento_duracion_ms):
        segmento = audio[i:i+segmento_duracion_ms]
        segmento_path = f"segmento_{i//segmento_duracion_ms}.wav"
        segmento.export(segmento_path, format="wav")
        segmentos.append(segmento_path)

    return segmentos

def transcribir_audio(audio_path):
    try:
        segmentos = dividir_audio(audio_path)
        texto_total = ""
        
        for segmento_path in segmentos:
            with open(segmento_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
                texto_total += transcript['text'] + " "
            
            os.remove(segmento_path)
        
        return texto_total.strip()
    except Exception as e:
        print(f"Error al transcribir el audio: {e}")
        return None

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    except Exception as e:
        print(f"Error al contar tokens: {e}")
        return 0

def traducir_texto(texto, source_lang="es", target_lang="en"):
    try:
        tokens_needed = num_tokens_from_string(texto, "gpt-3.5-turbo")
        print(f"Número de tokens necesarios para la traducción: {tokens_needed}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un traductor."},
                {"role": "user", "content": f"Translate the following text from {source_lang} to {target_lang}: {texto}"}
            ],
            max_tokens=tokens_needed + 100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error al traducir el texto: {e}")
        return None

def texto_a_voz(texto, lang="en"):
    try:
        tts = gTTS(text=texto, lang=lang)
        audio_path = "translated_audio.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error al convertir texto a voz: {e}")
        return None

def combinar_audio_video(video_path, audio_path):
    try:
        video = mp.VideoFileClip(video_path)
        audio = mp.AudioFileClip(audio_path)
        video = video.set_audio(audio)
        output_path = "output_video.mp4"
        video.write_videofile(output_path)
        return output_path
    except Exception as e:
        print(f"Error al combinar audio y video: {e}")
        return None

def main(video_path):
    audio_path = extraer_audio(video_path)
    if not audio_path:
        return

    texto = transcribir_audio(audio_path)
    if not texto:
        return

    texto_traducido = traducir_texto(texto)
    if not texto_traducido:
        return

    audio_traducido_path = texto_a_voz(texto_traducido)
    if not audio_traducido_path:
        return

    video_final_path = combinar_audio_video(video_path, audio_traducido_path)
    if video_final_path:
        print(f"Video traducido guardado en: {video_final_path}")
    else:
        print("Error en la generación del video final")

if __name__ == "__main__":
    video_path = "Lab_obs_lnd.mp4"
    main(video_path)
Versión Alternativa usando pyttsx3
Para usar pyttsx3 en lugar de gTTS para la síntesis de voz, puedes ejecuta el archivo app_pyttxsx3.py
