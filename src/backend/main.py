from fastapi import FastAPI
from routes.colorize import router as colorize_router

app = FastAPI(title="Palette Pilot API")

app.include_router(colorize_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
