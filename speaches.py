import openai
import io
import chainlit as cl

sst_model = "Systran/faster-distil-whisper-small.en"
# client = openai.AsyncClient(base_url='http://192.168.1.16:80/v1', api_key='lmao')

@cl.step(name='transcribe')
async def speech_to_text(speech: bytes) -> str:
    client = openai.AsyncClient(base_url='http://0.0.0.0:8870/v1', api_key='lmao')
    response = await client.audio.transcriptions.create(
        model=sst_model,
        file=io.BytesIO(speech),
    )
    return response.text

tts_model = "kokoro"
# tts_voice = "am_santa"  # old guy, pretty good
tts_voice = "af_bella" # good clear

@cl.step(name='about to speak')
async def text_to_speech(text: str) -> bytes:
    client = openai.AsyncClient(base_url='http://0.0.0.0:8880/v1', api_key='lmao')
    response = await client.audio.speech.create(
        model=tts_model,
        voice=tts_voice,
        input=text,
        response_format="wav",
        speed=1
    )
    return response.response.read()
