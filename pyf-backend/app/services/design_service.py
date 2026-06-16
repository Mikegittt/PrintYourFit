import httpx
import base64
from io import BytesIO
from PIL import Image
import asyncio

from app.core.config import settings

HF_MODEL = settings.HF_MODEL
HF_API_TOKEN = settings.HF_API_TOKEN

async def generate_image_from_prompt(prompt: str, num_inference_steps: int = 50) -> bytes | None:
    """
    Generate an image from a text prompt using Hugging Face Inference API.
    Returns PNG bytes or None if generation fails.
    """
    try:
        if not HF_API_TOKEN:
            print("Image generation error: HF_API_TOKEN is not configured. Set it in .env or Render environment variables.")
            return None
        if not HF_MODEL:
            print("Image generation error: HF_MODEL is not configured. Expected value like 'stabilityai/stable-diffusion-2'")
            return None

        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Accept": "image/png",
        }
        # include wait_for_model option to reduce transient failures
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True},
            "num_inference_steps": num_inference_steps,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            content_type = response.headers.get("content-type", "")
            if response.status_code == 200 and content_type.startswith("image"):
                return response.content  # bytes
            # If HF returns JSON with error details, log it for easier debugging
            try:
                txt = response.text
            except Exception:
                txt = '<unreadable response>'
            print(f"HF API error: status={response.status_code} content-type={content_type} body={txt}")
            return None
    except Exception as e:
        print(f"Image generation error: {e}")
        return None


def convert_image_format(image_bytes: bytes, from_format: str, to_format: str) -> bytes | None:
    """
    Convert image between formats (PNG, JPEG, WebP, etc.).
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        output = BytesIO()
        fmt = to_format.upper()
        if fmt == "JPG":
            fmt = "JPEG"
        img.save(output, format=fmt)
        return output.getvalue()
    except Exception as e:
        print(f"Format conversion error: {e}")
        return None
