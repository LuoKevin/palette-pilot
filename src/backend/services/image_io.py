import base64
from io import BytesIO

from PIL import Image
from fastapi import UploadFile


async def load_rgb_image(file: UploadFile) -> Image.Image:
    image_bytes = await file.read()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    return img


def image_to_base64_png(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
