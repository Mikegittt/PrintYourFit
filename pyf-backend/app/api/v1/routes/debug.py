from fastapi import APIRouter
import socket
import httpx
from app.core.config import settings

router = APIRouter()


@router.get("/hf-check")
async def hf_check():
    """Check DNS resolution and basic connectivity to the Hugging Face inference host."""
    host = "api-inference.huggingface.co"
    result = {"host": host}
    try:
        ip = socket.gethostbyname(host)
        result["dns"] = {"resolved": True, "ip": ip}
    except Exception as e:
        result["dns"] = {"resolved": False, "error": str(e)}

    # Try a simple HTTP request to the HF API root
    try:
        headers = {}
        token = settings.HF_API_TOKEN
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"https://{host}/models/{settings.HF_MODEL}", headers=headers)
            result["http"] = {"status_code": resp.status_code, "content_type": resp.headers.get("content-type", "")}
    except Exception as e:
        result["http"] = {"error": str(e)}

    return result
