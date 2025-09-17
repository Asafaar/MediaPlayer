# Video Player Controller

A web-based video player with FastAPI backend and React frontend. Control video playback through a web interface while the video displays locally using OpenCV.

## What it does

- Load and play local video files
- Control playback speed (0.5x, 1x, 2x, 4x)
- Play, pause, stop, and reset videos
- Real-time status updates
- Timestamp and speed overlays on video

## Installation
```bash
git clone https://github.com/Asafaar/MediaPlayer
cd MediaPlayer
```
### Backend (Python) 
```bash
cd backend
pip install -r requirements.txt
```

### Frontend (React)
```bash
cd frontend
npm install
```

## How to run

### 1. Start the backend server
```bash
cd backend
python main.py
```
Backend runs on: `http://127.0.0.1:8000`

### 2. Start the frontend
```bash
cd frontend
npm start
```
Frontend runs on: `http://127.0.0.1:3000`

## Usage

1. Open `http://127.0.0.1:3000` in your browser
2. Enter the path to a video file
3. Click "Load Video"
4. Use the web interface to control playback
5. Video displays locally in an OpenCV window

## Requirements

- Python 3.8+
- Node.js 16+
- OpenCV (for video display)
