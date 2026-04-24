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
