import webbrowser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pydantic import BaseModel
from env import (
    HOST_IP,
    PORT
)
# from core.model import Qwen3
# from core.tts import TTSVoice


model_map = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # model_map["llm"] = Qwen3()
    # model_map["tts"] = TTSVoice()

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


app.mount("/static", StaticFiles(directory="./web/static"), name="static")
templates = Jinja2Templates(directory="./web")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    webbrowser.open(f"http://{HOST_IP}:{PORT}")
    uvicorn.run(
        app,
        host=str(HOST_IP),
        port=int(PORT),
        # reload=True
    )

