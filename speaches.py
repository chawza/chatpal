import openai
import io
import chainlit as cl

from conf import load_conf

@cl.step(name='transcribe')
async def speech_to_text(speech: bytes) -> str:
    conf = load_conf()

    client = openai.AsyncClient(base_url=conf.SST_BASE_URL, api_key=conf.SST_KEY)
    response = await client.audio.transcriptions.create(
        model=conf.SST_MODEL_NAME,
        file=io.BytesIO(speech),
    )

    return response.text

@cl.step(name='about to speak')
async def text_to_speech(text: str) -> bytes:
    conf = load_conf()
    client = openai.AsyncClient(base_url=conf.TTS_BASE_URL, api_key=conf.TTS_KEY)

    response = await client.audio.speech.create(
        model=conf.TTS_MODEL_NAME,
        voice=conf.TTS_VOICE,
        input=text,
        response_format="wav",
        speed=1
    )

    return response.response.read()
