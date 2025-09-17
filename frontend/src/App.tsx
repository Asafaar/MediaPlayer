import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Load config
const config = require('./config.json');
const API_BASE_URL = `http://${config.backend.host}:${config.backend.port}`;

interface PlayerStatus {
  loaded: boolean;
  is_playing?: boolean;
  is_paused?: boolean;
  current_frame?: number;
  total_frames?: number;
  speed?: number;
  timestamp?: string;
}

function App() {
  const [videoPath, setVideoPath] = useState<string>('');
  const [status, setStatus] = useState<PlayerStatus>({ loaded: false });
  const [message, setMessage] = useState<string>('');

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/status`);
      setStatus(response.data);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleLoadVideo = async () => {
    if (!videoPath.trim()) {
      setMessage('Please enter a video path');
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/load_video`, null, {
        params: { video_path: videoPath }
      });
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error loading video');
    }
  };

  const handlePlay = async (speed?: number) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/play`,
        speed ? { speed } : {}
      );
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error playing video');
    }
  };

  const handlePause = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/pause`);
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error pausing video');
    }
  };

  const handleStop = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/stop`);
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error stopping video');
    }
  };

  const handleReset = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/reset`);
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error resetting video');
    }
  };

  const handleSetSpeed = async (speed: number) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/set_speed`, { speed });
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error setting speed');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Video Player Controller</h1>

        <div className="video-loader">
          <input
            type="text"
            placeholder="Enter video file path (e.g., C:\Users\...\video.mp4)"
            value={videoPath}
            onChange={(e) => setVideoPath(e.target.value)}
            className="video-input"
          />
          <button onClick={handleLoadVideo} className="control-button">
            Load Video
          </button>
        </div>

        {message && (
          <div className="message">
            <p>{message}</p>
          </div>
        )}

        {status.loaded && (
          <div className="status-info">
            <p>Status: {status.is_playing ? (status.is_paused ? 'Paused' : 'Playing') : 'Stopped'}</p>
            <p>Speed: {status.speed}x</p>
            <p>Time: {status.timestamp}</p>
            <p>Frame: {status.current_frame} / {status.total_frames}</p>
          </div>
        )}

        {status.loaded && (
          <div className="controls">
            <div className="control-section">
              <h3>Video Controls</h3>
              <div className="control-buttons">
                <button onClick={() => handlePlay()} className="control-button play">
                  {status.is_playing && !status.is_paused ? 'Resume' : 'Play'}
                </button>
                <button onClick={handlePause} className="control-button pause">
                  Pause
                </button>
                <button onClick={handleStop} className="control-button stop">
                  Stop
                </button>
                <button onClick={handleReset} className="control-button reset">
                  Reset
                </button>
              </div>
            </div>

            <div className="control-section">
              <h3>Speed Controls</h3>
              <div className="speed-controls">
                <div className="speed-buttons">
                  <button onClick={() => handleSetSpeed(0.5)} className="speed-button">
                    0.5x
                  </button>
                  <button onClick={() => handleSetSpeed(1)} className="speed-button">
                    1x
                  </button>
                  <button onClick={() => handleSetSpeed(2)} className="speed-button">
                    2x
                  </button>
                  <button onClick={() => handleSetSpeed(4)} className="speed-button">
                    4x
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
