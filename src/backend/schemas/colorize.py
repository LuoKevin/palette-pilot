from pydantic import BaseModel

class UploadInfo(BaseModel):
    filename: str | None
    content_type: str | None
    width: int | None = None
    height: int | None = None
    mode: str | None = None


class PipelineSettings(BaseModel):
    num_colors: int
    num_buckets: int
    lineart_threshold: int
    min_shade: float


class UploadResponse(BaseModel):
    target: UploadInfo
    reference: UploadInfo
    settings: PipelineSettings
    palette: list[list[int]]
    palette_counts: list[int]
    target_luminance_png_base64: str | None = None
    target_tone_buckets_png_base64: str | None = None
    recolored_image_png_base64: str | None = None
