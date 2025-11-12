import base64
from fastapi import (
    APIRouter,
    Request,
    HTTPException
)
from core.audio import Audio


router = APIRouter(
    prefix="/audio",
    tags=["audio"]
)
@router.get("/generate", summary="生成音频")
async def generate(request: Request, prompt: str):
    model: Audio = request.app.model_map.get("audio", None)

    if model is None:
        raise HTTPException(status_code=500, detail="Audio model not found")

    audio_bytes:bytes = model.to_audio(prompt)

    audio_base64: str = base64.b64encode(audio_bytes).decode("utf-8")

    return {"audio_base64": audio_base64}

