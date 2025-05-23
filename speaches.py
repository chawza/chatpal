import openai
import io

sst_model = "Systran/faster-distil-whisper-small.en"
tts_model = "hexgrad/Kokoro-82M"
tts_voice = "af_heart"
client = openai.AsyncClient(base_url='http://192.168.1.16:80/v1', api_key='lmao')

async def speech_to_text(speech: bytes) -> str:
    response = await client.audio.transcriptions.create(
        model=sst_model,
        file=io.BytesIO(speech),
    )
    return response.text

async def text_to_speech(text: str) -> bytes:
    response = await client.audio.speech.create(
        model=tts_model,
        voice=tts_voice,
        input=text,
        response_format="mp3",
        speed=1
    )
    return response.response.read()
