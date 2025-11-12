import json
from fastapi import (
    APIRouter,
    Request,
    HTTPException
)
from sse_starlette import EventSourceResponse
from core.model import Qwen3


router = APIRouter(
    prefix="/translate",
    tags=["translate"]
)


@router.get("/status", summary="获取翻译状态")
async def status(request: Request):
    model: Qwen3 = request.app.model_map.get("qwen3", None)

    if model is None:
        raise HTTPException(status_code=500, detail="Qwen3 model not found")

    return {"translating": model.is_generating}


@router.get("/generate", summary="生成翻译")
async def generate(request: Request, prompt: str):
    model: Qwen3 = request.app.model_map.get("qwen3", None)

    if model is None:
        raise HTTPException(status_code=500, detail="Qwen3 model not found")

    async def event_generator(
            request: Request,
            prompt: str
    ):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Please translate the user input into Chinese.",
            },
            {
                "role": "user", "content": prompt
            }
        ]
        for token in model.generate(messages):
            if await request.is_disconnected():
                print(f"/translate/start client disconnected")
            yield json.dumps({"token": token}, ensure_ascii=False)

    return EventSourceResponse(event_generator(request, prompt))


@router.get("/terminate", summary="终止翻译")
async def terminate(request: Request):
    model: Qwen3 = request.app.model_map.get("qwen3", None)
    if model is None:
        return
    model.terminate()
    print(f"/translate/terminate user terminated.")

