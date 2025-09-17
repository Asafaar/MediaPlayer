from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes.video import router as video_router
from app.config.settings import settings


app = FastAPI(title="Video Player API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router)



if __name__ == "__main__":
    host = settings.get("backend", {}).get("host", "0.0.0.0")
    port = settings.get("backend", {}).get("port", 8000)
    uvicorn.run(app, host=host, port=port)