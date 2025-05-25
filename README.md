An english conversation partner to practive english conversation

# Setup
## Setup Kokoro (TTS)
1. [kokoro](https://huggingface.co/hexgrad/Kokoro-82M) TTS as openai compatible server using [fast api kokor](https://github.com/remsky/Kokoro-FastAPI?tab=readme-ov-file)
2. [faster whisper](https://github.com/SYSTRAN/faster-whisper) STT as openai compatible server using [speaches](https://github.com/speaches-ai/speaches)
3. run this project using chainlit as using
    1. clone this project
        ```bash
        git clone https://github.com/chawza/chatpal.git
        cd chatpal
        ```
    2. install dependencies (UV recommended)
        ```bash
        uv sync
        ```
    3. run project!
        ```bash
        uv run chainlit run main.py  # add `-w` on project reload on code changes
        ```
    4. open web browser and go to `http://localhost:8000`
