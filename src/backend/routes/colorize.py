import base64
from fastapi import APIRouter, File, UploadFile
from schemas.colorize import UploadResponse, UploadInfo
from PIL import Image
from io import BytesIO
from services.palette import Palette, extract_palette
from services.preprocess import (
    compute_luminance,
    create_tone_bucket_map,
    visualize_tone_buckets,
)
from services.recolor import recolor_image

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

    num_colors = 5

    reference_palette: Palette = extract_palette(reference_img, num_colors=num_colors)
    reference_palette.sort_by_luminance()
    luminance_img = compute_luminance(target_img)
    luminance_base64 = image_to_base64_png(luminance_img)

    if not reference_palette.colors:
        raise ValueError("Reference image has no colors in its palette.")

    num_buckets = len(reference_palette.colors)

    tone_bucket_map = create_tone_bucket_map(luminance_img, num_buckets=num_buckets)

    tone_bucket_img = visualize_tone_buckets(tone_bucket_map, num_buckets=num_buckets)
    tone_bucket_base64 = image_to_base64_png(tone_bucket_img)

    recolored_img = recolor_image(tone_bucket_map, luminance_img, reference_palette.colors)
    recolored_base64 = image_to_base64_png(recolored_img)

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
        palette=reference_palette.colors,
        palette_counts=reference_palette.counts,
        target_luminance_png_base64=luminance_base64,
        target_tone_buckets_png_base64=tone_bucket_base64,
        recolored_image_png_base64=recolored_base64,
    )


async def load_rgb_image(file: UploadFile) -> Image.Image:
    image_bytes = await file.read()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    return img


def image_to_base64_png(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
