import os
from typing import Optional
from fastapi import HTTPException
from .media_player import MediaPlayer


class VideoService:
    def __init__(self):
        self.media_player: Optional[MediaPlayer] = None

    def load_video(self, video_path: str) -> dict:
        """Load a video file"""
        try:
            if not os.path.exists(video_path):
                raise HTTPException(status_code=404, detail="Video file not found")

            self.media_player = MediaPlayer(video_path)
            return {"message": "Video loaded successfully", "path": video_path}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def play_video(self, speed: Optional[float] = None) -> dict:
        """Play video with optional speed parameter"""
        if not self.media_player:
            raise HTTPException(status_code=400, detail="No video loaded")

        try:
            self.media_player.play(speed)
            return {"message": "Video playback started", "speed": self.media_player.speed}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def pause_video(self) -> dict:
        """Pause video playback"""
        if not self.media_player:
            raise HTTPException(status_code=400, detail="No video loaded")

        self.media_player.pause()
        return {"message": "Video playback paused"}

    def stop_video(self) -> dict:
        """Stop video playback"""
        if not self.media_player:
            raise HTTPException(status_code=400, detail="No video loaded")

        self.media_player.stop()
        return {"message": "Video playback stopped"}

    def reset_video(self) -> dict:
        """Reset video to beginning"""
        if not self.media_player:
            raise HTTPException(status_code=400, detail="No video loaded")

        self.media_player.reset()
        return {"message": "Video reset to beginning"}

    def set_speed(self, speed: float) -> dict:
        """Set playback speed"""
        if not self.media_player:
            raise HTTPException(status_code=400, detail="No video loaded")

        try:
            self.media_player.set_speed(speed)
            return {"message": f"Speed set to {speed}x", "speed": speed}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_status(self) -> dict:
        """Get current player status"""
        if not self.media_player:
            return {"loaded": False}

        status = self.media_player.get_status()
        status["loaded"] = True
        return status