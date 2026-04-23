from fastapi import APIRouter, File, UploadFile
from schemas.colorize import UploadResponse, UploadInfo

router = APIRouter(prefix="/colorize", tags=["colorize"])

@router.post("/upload")
def colorize(
    target_image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
) -> UploadResponse:
    target_info = UploadInfo(filename=target_image.filename, content_type=target_image.content_type)
    reference_info = UploadInfo(filename=reference_image.filename, content_type=reference_image.content_type)
    return UploadResponse(target=target_info, reference=reference_info)
