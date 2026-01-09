"""
Minimal test API server for testing frontend components
Implements V3.0 endpoints without audio transcription dependencies
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid
import json

app = FastAPI(title="Ecoute Test API", version="3.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
sessions = {}
settings = {
    "theme": "discord-dark",
    "llm_provider": "openai",
    "notification_enabled": True,
    "voice_commands_enabled": False
}

# Models
class CreateSessionRequest(BaseModel):
    name: str
    use_api: bool = True
    enable_search: bool = True

class ExportRequest(BaseModel):
    session_id: str
    format: str = "markdown"
    include_transcript: bool = True
    include_sources: bool = True
    include_insights: bool = True

class SearchHistoryRequest(BaseModel):
    query: str
    limit: int = 20

class SettingsUpdate(BaseModel):
    theme: Optional[str] = None
    llm_provider: Optional[str] = None
    notification_enabled: Optional[bool] = None
    voice_commands_enabled: Optional[bool] = None

# Initialize first session
first_session_id = str(uuid.uuid4())
sessions[first_session_id] = {
    "id": first_session_id,
    "name": "Default Session",
    "created_at": datetime.now().isoformat(),
    "is_active": True,
    "is_running": False,
    "transcript": "Welcome to Ecoute AI Research Assistant!",
    "response": "Hello! I'm ready to help you with research and insights.",
    "insights": {
        "key_topics": ["AI", "Research", "Productivity"],
        "action_items": [],
        "decisions_made": [],
        "questions_raised": []
    },
    "sources": []
}

@app.get("/")
def root():
    return {
        "name": "Ecoute Test API",
        "version": "3.0.0",
        "status": "running"
    }

@app.get("/status")
def status():
    return {
        "status": "ok",
        "sessions_count": len(sessions),
        "active_session": next((s["id"] for s in sessions.values() if s["is_active"]), None)
    }

# Session Management
@app.post("/sessions")
def create_session(request: CreateSessionRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "id": session_id,
        "name": request.name,
        "created_at": datetime.now().isoformat(),
        "is_active": False,
        "is_running": False,
        "transcript": "",
        "response": "",
        "insights": {"key_topics": [], "action_items": [], "decisions_made": [], "questions_raised": []},
        "sources": []
    }
    return {"session_id": session_id, "status": "created"}

@app.get("/sessions")
def list_sessions():
    return {
        "sessions": [
            {
                "id": s["id"],
                "name": s["name"],
                "created_at": s["created_at"],
                "is_active": s["is_active"],
                "is_running": s["is_running"]
            }
            for s in sessions.values()
        ]
    }

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "deleted"}
    return {"status": "not_found"}

@app.post("/sessions/{session_id}/activate")
def activate_session(session_id: str):
    if session_id in sessions:
        # Deactivate all others
        for s in sessions.values():
            s["is_active"] = False
        sessions[session_id]["is_active"] = True
        return {"status": "activated"}
    return {"status": "not_found"}

@app.post("/sessions/{session_id}/start")
def start_session(session_id: str):
    if session_id in sessions:
        sessions[session_id]["is_running"] = True
        return {"status": "started"}
    return {"status": "not_found"}

@app.post("/sessions/{session_id}/stop")
def stop_session(session_id: str):
    if session_id in sessions:
        sessions[session_id]["is_running"] = False
        return {"status": "stopped"}
    return {"status": "not_found"}

@app.get("/sessions/{session_id}/transcript")
def get_transcript(session_id: str):
    if session_id in sessions:
        return {"transcript": sessions[session_id]["transcript"]}
    return {"transcript": ""}

@app.get("/sessions/{session_id}/response")
def get_response(session_id: str):
    if session_id in sessions:
        return {"response": sessions[session_id]["response"]}
    return {"response": ""}

@app.get("/sessions/{session_id}/insights")
def get_insights(session_id: str):
    if session_id in sessions:
        return {"insights": sessions[session_id]["insights"]}
    return {"insights": {}}

# Export
@app.post("/export")
def export_session(request: ExportRequest):
    if request.session_id not in sessions:
        return {"error": "Session not found"}

    session = sessions[request.session_id]

    if request.format == "markdown":
        content = f"# {session['name']}\n\n"
        if request.include_transcript:
            content += f"## Transcript\n\n{session['transcript']}\n\n"
        if request.include_sources:
            content += f"## Sources\n\n{len(session['sources'])} sources found\n\n"
        if request.include_insights:
            content += f"## Insights\n\n"
            content += f"Topics: {', '.join(session['insights']['key_topics'])}\n"
    elif request.format == "json":
        content = json.dumps(session, indent=2)
    elif request.format == "html":
        content = f"<html><body><h1>{session['name']}</h1></body></html>"
    else:
        content = "Unknown format"

    return {
        "content": content,
        "format": request.format,
        "filename": f"{session['name']}.{request.format}"
    }

# Search
@app.post("/search/history")
def search_history(request: SearchHistoryRequest):
    results = []
    for session in sessions.values():
        if request.query.lower() in session["transcript"].lower() or \
           request.query.lower() in session["name"].lower():
            results.append({
                "session_id": session["id"],
                "session_name": session["name"],
                "created_at": session["created_at"],
                "preview": session["transcript"][:200]
            })

    return {"results": results[:request.limit]}

# Settings
@app.get("/settings")
def get_settings():
    return settings

@app.post("/settings")
def update_settings(update: SettingsUpdate):
    if update.theme:
        settings["theme"] = update.theme
    if update.llm_provider:
        settings["llm_provider"] = update.llm_provider
    if update.notification_enabled is not None:
        settings["notification_enabled"] = update.notification_enabled
    if update.voice_commands_enabled is not None:
        settings["voice_commands_enabled"] = update.voice_commands_enabled

    return {"status": "updated", "settings": settings}

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send updates every 2 seconds
            active_session = next((s for s in sessions.values() if s["is_active"]), None)
            if active_session:
                await websocket.send_json({
                    "type": "update",
                    "transcript": active_session["transcript"],
                    "response": active_session["response"],
                    "research_status": {
                        "active_searches": [],
                        "recent_searches": []
                    },
                    "sources": active_session["sources"],
                    "insights": active_session["insights"]
                })

            # Wait for client messages
            try:
                data = await websocket.receive_text()
            except:
                break
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
