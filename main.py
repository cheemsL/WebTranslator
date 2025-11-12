import webbrowser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from env import (
    HOST_IP,
    PORT
)
from api import (
    translate,
    audio
)
from core.model import Qwen3
from core.audio import Audio


model_map = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_map["qwen3"] = Qwen3()
    model_map["audio"] = Audio()
    model_map["message"] = "Hello World"

    yield

    model_map.clear()


app = FastAPI(
    lifespan=lifespan,
)
app.model_map = model_map


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


app.mount("/static", StaticFiles(directory="./web/static"), name="static")
templates = Jinja2Templates(directory="./web")


app.include_router(translate.router)
app.include_router(audio.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    # webbrowser.open(f"http://{HOST_IP}:{PORT}")
    uvicorn.run(
        app,
        host=str(HOST_IP),
        port=int(PORT),
        # reload=True
    )

