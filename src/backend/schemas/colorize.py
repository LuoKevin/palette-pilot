from pydantic import BaseModel

class UploadInfo(BaseModel):
    filename: str | None
    content_type: str | None

class UploadResponse(BaseModel):
    target: UploadInfo
    reference: UploadInfo
