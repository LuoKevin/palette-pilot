from fastapi import APIRouter


router = APIRouter(prefix="/colorize", tags=["colorize"])

@router.get("/")
def colorize() -> dict[str, str]:
    return {"message": "Colorize endpoint"}