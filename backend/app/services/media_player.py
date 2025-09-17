"""
MediaPlayer class for video playback with OpenCV.

This module provides a MediaPlayer class that handles video file loading,
playback control, and frame display with timestamp overlays.
"""

import cv2
import threading
import time
from typing import Optional, Dict, Any


class MediaPlayer:
    """
    A video player class that provides playback control and frame display.

    This class uses OpenCV to handle video files and provides functionality
    for playing, pausing, stopping, and controlling playback speed.
    """

    # Valid playback speeds supported by the player
    VALID_SPEEDS = [0.5, 1.0, 2.0, 4.0]

    def __init__(self, video_path: str) -> None:
        """
        Initialize the MediaPlayer with a video file.

        Args:
            video_path (str): Path to the video file to be played

        Raises:
            ValueError: If the video file cannot be opened
        """
        self.video_path = video_path
        self.cap = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 30.0
        self.speed = 1.0  # Default speed changed to 1x for better UX
        self.play_thread = None
        self._load_video()

    def _load_video(self) -> None:
        """
        Load the video file and extract basic properties.

        Raises:
            ValueError: If the video file cannot be opened
        """
        if self.cap:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        if self.fps <= 0:
            self.fps = 30.0  # Fallback FPS if video doesn't provide it

    def play(self, speed: Optional[float] = None) -> None:
        """
        Start or resume video playback.

        Args:
            speed (Optional[float]): Playback speed to set before playing
        """
        if speed is not None:
            self.set_speed(speed)

        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.play_thread = threading.Thread(target=self._play_video)
            self.play_thread.daemon = True
            self.play_thread.start()
        else:
            self.is_paused = False

    def pause(self) -> None:
        """Pause video playback if currently playing."""
        if self.is_playing:
            self.is_paused = True

    def stop(self) -> None:
        """Stop video playback completely and close display windows."""
        self.is_playing = False
        self.is_paused = False
        if self.play_thread:
            self.play_thread.join()
        cv2.destroyAllWindows()

    def reset(self) -> None:
        """Reset video to the beginning."""
        self.stop()
        self.current_frame = 0
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def set_speed(self, speed: float) -> None:
        """
        Set playback speed.

        Args:
            speed (float): Playback speed multiplier

        Raises:
            ValueError: If speed is not a valid option
        """
        if speed in self.VALID_SPEEDS:
            self.speed = speed
        else:
            raise ValueError(f"Invalid speed. Must be one of: {self.VALID_SPEEDS}")

    def _play_video(self) -> None:
        """
        Internal method to handle video frame playback in a separate thread.

        This method runs in a loop while playing, reading frames from the video,
        adding overlays, and displaying them at the correct timing.
        """
        while self.is_playing and self.cap and self.cap.isOpened():
            if self.is_paused:
                time.sleep(0.1)  # Short sleep while paused
                continue

            ret, frame = self.cap.read()
            if not ret:
                # End of video reached
                break

            # Add visual overlays to the frame
            self._add_overlays(frame)

            # Display the frame
            cv2.imshow('Video Player', frame)

            # Calculate and apply frame delay based on speed
            frame_delay = (1.0 / self.fps) / self.speed
            time.sleep(frame_delay)

            self.current_frame += 1

            # Check for quit command (ESC or 'q')
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), 27]:  # 'q' or ESC key
                break

        self.is_playing = False
        cv2.destroyAllWindows()

    def _add_overlays(self, frame) -> None:
        """
        Add timestamp and speed overlays to the video frame.

        Args:
            frame: The video frame to add overlays to
        """
        # Add timestamp overlay (top-left)
        timestamp = self._get_timestamp()
        cv2.putText(
            frame, timestamp, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
        )

        # Add speed overlay (below timestamp)
        speed_text = f"Speed: {self.speed}x"
        cv2.putText(
            frame, speed_text, (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
        )

    def _get_timestamp(self) -> str:
        """
        Get current playback timestamp as a formatted string.

        Returns:
            str: Timestamp in MM:SS:mmm format
        """
        if self.fps > 0:
            current_time = self.current_frame / self.fps
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            milliseconds = int((current_time % 1) * 1000)
            return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
        return "00:00:000"

    def get_status(self) -> Dict[str, Any]:
        """
        Get current player status information.

        Returns:
            Dict[str, Any]: Dictionary containing player state information
        """
        return {
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "current_frame": self.current_frame,
            "total_frames": self.total_frames,
            "speed": self.speed,
            "timestamp": self._get_timestamp(),
            "video_path": self.video_path,
            "fps": self.fps
        }

    def __del__(self) -> None:
        """Cleanup resources when object is destroyed."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()