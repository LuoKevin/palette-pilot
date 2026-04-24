from fastapi import APIRouter, File, UploadFile
from schemas.colorize import UploadResponse, UploadInfo
from PIL import Image
from io import BytesIO


router = APIRouter(prefix="/colorize", tags=["colorize"])

@router.post("/upload")
async def colorize(
    target_image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
) -> UploadResponse:

    target_img = await load_rgb_image(target_image)
    reference_img = await load_rgb_image(reference_image)

    target_width, target_height = target_img.size
    reference_width, reference_height = reference_img.size
    target_mode = target_img.mode
    reference_mode = reference_img.mode

    return UploadResponse(
        target=UploadInfo(
            filename=target_image.filename,
            content_type=target_image.content_type,
            width=target_width,
            height=target_height,
            mode=target_mode,
        ),
        reference=UploadInfo(
            filename=reference_image.filename,
            content_type=reference_image.content_type,
            width=reference_width,
            height=reference_height,
            mode=reference_mode,
        ),
    )


async def load_rgb_image(file: UploadFile) -> Image.Image:
    image_bytes = await file.read()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    return img

