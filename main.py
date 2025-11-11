import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from env import (
    HOST_IP,
    PORT
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


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


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=str(HOST_IP),
        port=int(PORT),
        # reload=True
    )

