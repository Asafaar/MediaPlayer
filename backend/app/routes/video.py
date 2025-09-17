from fastapi import APIRouter, HTTPException
from app.models.requests import PlayRequest, SpeedRequest
from app.services.video_service import VideoService

router = APIRouter(tags=["video"])

video_service = VideoService()


@router.post("/load_video")
async def load_video(video_path: str):
    """Load a video file"""
    return video_service.load_video(video_path)


@router.post("/play")
async def play_video(request: PlayRequest = PlayRequest()):
    """Play video with optional speed parameter"""
    return video_service.play_video(request.speed)


@router.post("/pause")
async def pause_video():
    """Pause video playback"""
    return video_service.pause_video()


@router.post("/stop")
async def stop_video():
    """Stop video playback"""
    return video_service.stop_video()


@router.post("/reset")
async def reset_video():
    """Reset video to beginning"""
    return video_service.reset_video()


@router.post("/set_speed")
async def set_speed(request: SpeedRequest):
    """Set playback speed"""
    return video_service.set_speed(request.speed)


@router.get("/status")
async def get_status():
    """Get current player status"""
    return video_service.get_status()