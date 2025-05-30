from typing import TYPE_CHECKING
import io
import os
from os import path
from chainlit.message import Message
import openai
import wave
import asyncio
import chainlit as cl
from conf import load_conf
import speaches
import utils
import prompts

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


@cl.step(name='processing')
async def complete(messages: 'list[ChatCompletionMessageParam]') -> str:
    conf = load_conf()

    client = openai.AsyncClient(base_url=conf.OPENAI_BASE_URL, api_key=conf.OPENAI_TOKEN)
    response = await client.chat.completions.create(model=conf.LLM_MODEL, messages=messages)
    content = response.choices[0].message.content

    if not content:
        raise Exception('Invalid LLM Output: Empty')

    return content

@cl.on_chat_start
async def main():
    cl.chat_context.add(cl.Message(type="system_message", content=prompts.system_prompt))
    await cl.Message(type="assistant_message", content="Hello, who can I help you?").send()

@cl.on_audio_start
async def on_audio_start():
    cl.user_session.set("audio_chunks", [])
    return True

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.InputAudioChunk):
    chunks: list[bytes] = cl.user_session.get('audio_chunks', [])  # type: ignore
    chunks.append(chunk.data)
    cl.user_session.set('audio_chunks', chunks)

@cl.on_audio_end
async def on_audio_end():
    chunks: list[bytes] = cl.user_session.get('audio_chunks', [])  # type: ignore

    if not chunks:
        return

    audio_buffer = io.BytesIO()

    with wave.open(audio_buffer, 'wb') as file:
        file.setnchannels(1)
        file.setframerate(24_000)
        file.setsampwidth(2)
        file.writeframes(b''.join(chunks))
        audio_buffer.seek(0)

    audio_bytes = audio_buffer.read()

    sound_replay_element = cl.Audio(content=audio_bytes, mime="audio/wav")
    transcribed = await speaches.speech_to_text(audio_bytes)
    await cl.Message(author="You", type='user_message', elements=[sound_replay_element], content=transcribed).send()
    # cl.chat_context.add(cl.Message(type='user_message', content=transcribed))

    llm_response_str = await complete(cl.chat_context.to_openai()) or ''
    assert llm_response_str, 'Invalid LLM Response'

    output_speech_bytes = await speaches.text_to_speech(text=llm_response_str)

    output_llm_audio = cl.Audio(content=output_speech_bytes, mime='audio/wav', auto_play=True)
    await cl.Message(type='assistant_message', content=llm_response_str, elements=[output_llm_audio]).send()
