from pydantic import BaseModel

class UploadInfo(BaseModel):
    filename: str | None
    content_type: str | None
    width: int | None = None
    height: int | None = None
    mode: str | None = None

class UploadResponse(BaseModel):
    target: UploadInfo
    reference: UploadInfo
    palette: list[list[int]]
    palette_counts: list[int]
    target_luminance_png_base64: str | None = None
    target_tone_buckets_png_base64: str | None = None