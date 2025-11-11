import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from env import (
    HOST_IP,
    PORT
)
from core.model import Qwen3
from core.tts import TTSVoice


model_map = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_map["llm"] = Qwen3()
    model_map["tts"] = TTSVoice()

    yield

    model_map.clear()


app = FastAPI(
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


@app.get("/")
async def root():
    return "Hello World!"


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=str(HOST_IP),
        port=int(PORT),
        # reload=True
    )

