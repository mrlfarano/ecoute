"""
FastAPI backend server for Ecoute Electron app
Handles audio transcription, AI responses, and research
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import threading
import queue
import sys
import os
from typing import Optional, List, Dict

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder
from SearchEngine import SearchEngine
from ActionTracker import ActionTracker
import AudioRecorder
import TranscriberModels

app = FastAPI(title="Ecoute API", version="2.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class AppState:
    def __init__(self):
        self.transcriber = None
        self.responder = None
        self.speaker_queue = None
        self.mic_queue = None
        self.is_running = False
        self.websocket_clients = []

state = AppState()

# Pydantic models
class StartSessionRequest(BaseModel):
    use_api: bool = False
    enable_search: bool = True

class DeepDiveRequest(BaseModel):
    topic: str

class ConfigUpdate(BaseModel):
    api_key: Optional[str] = None

# Routes
@app.get("/")
async def root():
    return {
        "name": "Ecoute API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/status")
async def get_status():
    return {
        "is_running": state.is_running,
        "has_transcriber": state.transcriber is not None,
        "has_responder": state.responder is not None
    }

@app.post("/session/start")
async def start_session(request: StartSessionRequest):
    """Start transcription and AI response session"""
    if state.is_running:
        return {"status": "already_running"}

    try:
        # Initialize queues
        state.speaker_queue = queue.Queue()
        state.mic_queue = queue.Queue()

        # Initialize audio recorders
        user_audio_recorder = AudioRecorder.DefaultMicRecorder()
        user_audio_recorder.record_into_queue(state.mic_queue)

        await asyncio.sleep(2)

        speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
        speaker_audio_recorder.record_into_queue(state.speaker_queue)

        # Initialize model
        model = TranscriberModels.get_model(request.use_api)

        # Initialize transcriber
        state.transcriber = AudioTranscriber(
            user_audio_recorder.source,
            speaker_audio_recorder.source,
            model
        )

        # Start transcription thread
        transcribe_thread = threading.Thread(
            target=state.transcriber.transcribe_audio_queue,
            args=(state.speaker_queue, state.mic_queue),
            daemon=True
        )
        transcribe_thread.start()

        # Initialize GPT responder
        state.responder = GPTResponder(enable_search=request.enable_search)
        responder_thread = threading.Thread(
            target=state.responder.respond_to_transcriber,
            args=(state.transcriber,),
            daemon=True
        )
        responder_thread.start()

        state.is_running = True

        return {
            "status": "started",
            "use_api": request.use_api,
            "search_enabled": request.enable_search
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/stop")
async def stop_session():
    """Stop the current session"""
    if not state.is_running:
        return {"status": "not_running"}

    state.is_running = False
    state.transcriber = None
    state.responder = None

    return {"status": "stopped"}

@app.get("/transcript")
async def get_transcript():
    """Get current transcript"""
    if not state.transcriber:
        raise HTTPException(status_code=400, detail="No active session")

    transcript = state.transcriber.get_transcript()
    return {"transcript": transcript}

@app.get("/response")
async def get_response():
    """Get current AI response"""
    if not state.responder:
        raise HTTPException(status_code=400, detail="No active session")

    return {
        "response": str(state.responder.response),
        "sources": [s.to_dict() for s in state.responder.sources]
    }

@app.get("/research/status")
async def get_research_status():
    """Get current research activity"""
    if not state.responder:
        raise HTTPException(status_code=400, detail="No active session")

    return state.responder.get_research_status()

@app.get("/research/sources")
async def get_sources():
    """Get all research sources"""
    if not state.responder or not state.responder.search_engine:
        return {"sources": []}

    sources = state.responder.search_engine.get_all_sources()
    return {"sources": [s.to_dict() for s in sources]}

@app.get("/insights")
async def get_insights():
    """Get conversation insights and action items"""
    if not state.responder:
        raise HTTPException(status_code=400, detail="No active session")

    insights = state.responder.action_tracker.conversation_insights
    return {
        "key_topics": insights.key_topics,
        "decisions_made": insights.decisions_made,
        "questions_raised": insights.questions_raised,
        "action_items": [
            {
                "text": item.text,
                "priority": item.priority,
                "assigned_to": item.assigned_to,
                "completed": item.completed
            }
            for item in insights.action_items
        ]
    }

@app.post("/deep-dive")
async def deep_dive(request: DeepDiveRequest):
    """Perform deep dive research on a topic"""
    if not state.responder or not state.responder.search_engine:
        raise HTTPException(status_code=400, detail="Search not available")

    try:
        result = state.responder.search_engine.research_topic(request.topic)
        return {
            "topic": request.topic,
            "queries": result.get('queries', []),
            "sources": [s.to_dict() for s in result.get('sources', [])],
            "has_research": result.get('has_research', False)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_context():
    """Clear conversation context"""
    if state.transcriber:
        state.transcriber.clear_transcript_data()

    if state.responder:
        state.responder.clear_context()

    if state.speaker_queue:
        with state.speaker_queue.mutex:
            state.speaker_queue.queue.clear()

    if state.mic_queue:
        with state.mic_queue.mutex:
            state.mic_queue.queue.clear()

    return {"status": "cleared"}

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state.websocket_clients.append(websocket)

    try:
        while True:
            # Send updates every 500ms
            await asyncio.sleep(0.5)

            if state.is_running and state.transcriber and state.responder:
                data = {
                    "type": "update",
                    "transcript": state.transcriber.get_transcript(),
                    "response": str(state.responder.response),
                    "research_status": state.responder.get_research_status(),
                    "sources": [s.to_dict() for s in state.responder.sources],
                }

                # Get insights
                insights = state.responder.action_tracker.conversation_insights
                data["insights"] = {
                    "key_topics": insights.key_topics,
                    "decisions_made": insights.decisions_made,
                    "questions_raised": insights.questions_raised,
                    "action_items": [
                        {
                            "text": item.text,
                            "priority": item.priority,
                            "assigned_to": item.assigned_to,
                            "completed": item.completed
                        }
                        for item in insights.action_items
                    ]
                }

                await websocket.send_json(data)

    except WebSocketDisconnect:
        state.websocket_clients.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in state.websocket_clients:
            state.websocket_clients.remove(websocket)

if __name__ == "__main__":
    print("Starting Ecoute API Server...")
    print("Server running on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
