import pydantic
import os
from functools import cache

class Conf(pydantic.BaseModel):
    LLM_MODEL: str
    OPENAI_BASE_URL: str
    OPENAI_TOKEN: str

    SST_BASE_URL: str
    SST_MODEL_NAME: str
    SST_KEY: str

    TTS_BASE_URL: str
    TTS_MODEL_NAME: str
    TTS_VOICE: str
    TTS_KEY: str

@cache
def load_conf():
    params = {}
    for name in Conf.model_fields.keys():
        params[name] = os.environ.get(name, None)
    return Conf(**params)
