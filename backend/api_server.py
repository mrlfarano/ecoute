"""
Enhanced FastAPI backend server for Ecoute Electron app
Supports multiple sessions, integrations, and advanced features
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
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder
from SearchEngine import SearchEngine
from ActionTracker import ActionTracker
import AudioRecorder
import TranscriberModels

app = FastAPI(title="Ecoute API", version="3.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    JSON = "json"
    HTML = "html"

# Session management
class Session:
    def __init__(self, session_id: str, name: str):
        self.id = session_id
        self.name = name
        self.created_at = datetime.now()
        self.transcriber = None
        self.responder = None
        self.speaker_queue = None
        self.mic_queue = None
        self.is_running = False
        self.metadata = {}

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.active_session_id: Optional[str] = None

    def create_session(self, name: str) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id, name)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.active_session_id == session_id:
                self.active_session_id = None

    def list_sessions(self) -> List[Dict]:
        return [
            {
                "id": s.id,
                "name": s.name,
                "created_at": s.created_at.isoformat(),
                "is_running": s.is_running,
                "is_active": s.id == self.active_session_id
            }
            for s in self.sessions.values()
        ]

session_manager = SessionManager()
websocket_clients = []

# Pydantic models
class CreateSessionRequest(BaseModel):
    name: str
    use_api: bool = False
    enable_search: bool = True
    llm_provider: LLMProvider = LLMProvider.OPENAI

class StartSessionRequest(BaseModel):
    session_id: str

class ExportRequest(BaseModel):
    session_id: str
    format: ExportFormat
    include_transcript: bool = True
    include_sources: bool = True
    include_insights: bool = True

class SearchHistoryRequest(BaseModel):
    query: str
    limit: int = 20

class EmailDraftRequest(BaseModel):
    session_id: str
    recipient: Optional[str] = None
    subject: Optional[str] = None

class TaskIntegrationRequest(BaseModel):
    session_id: str
    provider: str  # "jira", "asana", "todoist", etc.
    action_item_id: int

class VoiceCommandRequest(BaseModel):
    command: str
    context: Optional[Dict] = None

class SettingsUpdate(BaseModel):
    theme: Optional[str] = None
    api_key: Optional[str] = None
    llm_provider: Optional[str] = None
    notification_enabled: Optional[bool] = None
    voice_commands_enabled: Optional[bool] = None

# Global settings
settings = {
    "theme": "discord-dark",
    "llm_provider": "openai",
    "notification_enabled": True,
    "voice_commands_enabled": False,
    "keyboard_shortcuts": {},
}

# Routes
@app.get("/")
async def root():
    return {
        "name": "Ecoute API Enhanced",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "multi-session",
            "search-history",
            "export",
            "integrations",
            "voice-commands",
            "multi-llm"
        ]
    }

@app.get("/status")
async def get_status():
    active_session = session_manager.get_session(session_manager.active_session_id) if session_manager.active_session_id else None
    return {
        "active_session_id": session_manager.active_session_id,
        "is_running": active_session.is_running if active_session else False,
        "total_sessions": len(session_manager.sessions),
        "settings": settings
    }

# Session Management
@app.post("/sessions")
async def create_session(request: CreateSessionRequest):
    """Create a new session"""
    session = session_manager.create_session(request.name)
    return {
        "session_id": session.id,
        "name": session.name,
        "created_at": session.created_at.isoformat()
    }

@app.get("/sessions")
async def list_sessions():
    """List all sessions"""
    return {"sessions": session_manager.list_sessions()}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    session_manager.delete_session(session_id)
    return {"status": "deleted"}

@app.post("/sessions/{session_id}/start")
async def start_session(session_id: str, use_api: bool = False, enable_search: bool = True):
    """Start a specific session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.is_running:
        return {"status": "already_running"}

    try:
        # Initialize queues
        session.speaker_queue = queue.Queue()
        session.mic_queue = queue.Queue()

        # Initialize audio recorders
        user_audio_recorder = AudioRecorder.DefaultMicRecorder()
        user_audio_recorder.record_into_queue(session.mic_queue)

        await asyncio.sleep(2)

        speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
        speaker_audio_recorder.record_into_queue(session.speaker_queue)

        # Initialize model
        model = TranscriberModels.get_model(use_api)

        # Initialize transcriber
        session.transcriber = AudioTranscriber(
            user_audio_recorder.source,
            speaker_audio_recorder.source,
            model
        )

        # Start transcription thread
        transcribe_thread = threading.Thread(
            target=session.transcriber.transcribe_audio_queue,
            args=(session.speaker_queue, session.mic_queue),
            daemon=True
        )
        transcribe_thread.start()

        # Initialize GPT responder
        session.responder = GPTResponder(enable_search=enable_search)
        responder_thread = threading.Thread(
            target=session.responder.respond_to_transcriber,
            args=(session.transcriber,),
            daemon=True
        )
        responder_thread.start()

        session.is_running = True
        session_manager.active_session_id = session_id

        return {
            "status": "started",
            "session_id": session_id,
            "use_api": use_api,
            "search_enabled": enable_search
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions/{session_id}/stop")
async def stop_session(session_id: str):
    """Stop a session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.is_running = False
    return {"status": "stopped"}

@app.post("/sessions/{session_id}/activate")
async def activate_session(session_id: str):
    """Set a session as active (for viewing)"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_manager.active_session_id = session_id
    return {"status": "activated", "session_id": session_id}

# Data retrieval
@app.get("/sessions/{session_id}/transcript")
async def get_transcript(session_id: str):
    """Get session transcript"""
    session = session_manager.get_session(session_id)
    if not session or not session.transcriber:
        raise HTTPException(status_code=400, detail="No active transcription")

    transcript = session.transcriber.get_transcript()
    return {"transcript": transcript}

@app.get("/sessions/{session_id}/response")
async def get_response(session_id: str):
    """Get AI response"""
    session = session_manager.get_session(session_id)
    if not session or not session.responder:
        raise HTTPException(status_code=400, detail="No active responder")

    return {
        "response": str(session.responder.response),
        "sources": [s.to_dict() for s in session.responder.sources]
    }

@app.get("/sessions/{session_id}/insights")
async def get_insights(session_id: str):
    """Get conversation insights"""
    session = session_manager.get_session(session_id)
    if not session or not session.responder:
        raise HTTPException(status_code=400, detail="No active session")

    insights = session.responder.action_tracker.conversation_insights
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

# Export functionality
@app.post("/export")
async def export_session(request: ExportRequest):
    """Export session in various formats"""
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    export_data = {
        "session_name": session.name,
        "created_at": session.created_at.isoformat(),
    }

    if request.include_transcript and session.transcriber:
        export_data["transcript"] = session.transcriber.get_transcript()

    if request.include_sources and session.responder:
        export_data["sources"] = [s.to_dict() for s in session.responder.sources]

    if request.include_insights and session.responder:
        insights = session.responder.action_tracker.conversation_insights
        export_data["insights"] = {
            "key_topics": insights.key_topics,
            "decisions_made": insights.decisions_made,
            "questions_raised": insights.questions_raised,
            "action_items": [
                {
                    "text": item.text,
                    "priority": item.priority,
                    "assigned_to": item.assigned_to
                }
                for item in insights.action_items
            ]
        }

    if request.format == ExportFormat.MARKDOWN:
        return {"format": "markdown", "content": _generate_markdown(export_data)}
    elif request.format == ExportFormat.JSON:
        return {"format": "json", "content": json.dumps(export_data, indent=2)}
    elif request.format == ExportFormat.HTML:
        return {"format": "html", "content": _generate_html(export_data)}

    return export_data

def _generate_markdown(data: Dict) -> str:
    """Generate markdown export"""
    md = f"# {data['session_name']}\n\n"
    md += f"**Date:** {data['created_at']}\n\n"

    if "transcript" in data:
        md += "## Transcript\n\n"
        md += data["transcript"] + "\n\n"

    if "insights" in data:
        insights = data["insights"]
        md += "## Insights\n\n"

        if insights.get("key_topics"):
            md += "### Key Topics\n\n"
            for topic in insights["key_topics"]:
                md += f"- {topic}\n"
            md += "\n"

        if insights.get("action_items"):
            md += "### Action Items\n\n"
            for item in insights["action_items"]:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(item["priority"], "⚪")
                md += f"- {priority_emoji} **{item['assigned_to']}**: {item['text']}\n"
            md += "\n"

    if "sources" in data:
        md += "## Sources\n\n"
        for i, source in enumerate(data["sources"], 1):
            md += f"{i}. **{source['title']}**\n"
            md += f"   {source['snippet']}\n\n"

    return md

def _generate_html(data: Dict) -> str:
    """Generate HTML export"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data['session_name']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1, h2, h3 {{ color: #333; }}
            .meta {{ color: #666; font-size: 14px; }}
            .action-item {{ padding: 10px; margin: 5px 0; border-left: 3px solid #5865f2; }}
        </style>
    </head>
    <body>
        <h1>{data['session_name']}</h1>
        <p class="meta">Date: {data['created_at']}</p>
    """

    if "transcript" in data:
        html += f"<h2>Transcript</h2><pre>{data['transcript']}</pre>"

    if "insights" in data and data["insights"].get("action_items"):
        html += "<h2>Action Items</h2>"
        for item in data["insights"]["action_items"]:
            html += f'<div class="action-item"><strong>{item["assigned_to"]}</strong>: {item["text"]}</div>'

    html += "</body></html>"
    return html

# Email drafting
@app.post("/email/draft")
async def draft_email(request: EmailDraftRequest):
    """Generate email draft from session"""
    session = session_manager.get_session(request.session_id)
    if not session or not session.responder:
        raise HTTPException(status_code=404, detail="Session not found")

    # Generate email using GPT
    from openai import OpenAI
    try:
        from keys import OPENAI_API_KEY
        client = OpenAI(api_key=OPENAI_API_KEY)
    except:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    transcript = session.transcriber.get_transcript() if session.transcriber else ""
    insights = session.responder.action_tracker.conversation_insights

    prompt = f"""Based on this meeting conversation, draft a professional follow-up email.

Transcript:
{transcript[:2000]}

Action Items:
{chr(10).join([f'- {item.text}' for item in insights.action_items])}

Generate a professional email with:
- Clear subject line
- Friendly greeting
- Brief summary
- Action items list
- Professional closing

Keep it concise and professional."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    draft = response.choices[0].message.content

    return {
        "subject": request.subject or "Meeting Follow-up",
        "to": request.recipient,
        "body": draft
    }

# Voice commands
@app.post("/voice/command")
async def process_voice_command(request: VoiceCommandRequest):
    """Process voice command"""
    command = request.command.lower()

    if "deep dive" in command or "research" in command:
        # Extract topic
        topic = command.replace("deep dive", "").replace("research", "").strip()
        return {"action": "deep_dive", "topic": topic}

    elif "summarize" in command:
        return {"action": "summarize"}

    elif "export" in command:
        return {"action": "export"}

    elif "new session" in command or "create session" in command:
        return {"action": "new_session"}

    return {"action": "unknown", "command": command}

# Settings
@app.get("/settings")
async def get_settings():
    """Get current settings"""
    return settings

@app.post("/settings")
async def update_settings(update: SettingsUpdate):
    """Update settings"""
    if update.theme:
        settings["theme"] = update.theme
    if update.llm_provider:
        settings["llm_provider"] = update.llm_provider
    if update.notification_enabled is not None:
        settings["notification_enabled"] = update.notification_enabled
    if update.voice_commands_enabled is not None:
        settings["voice_commands_enabled"] = update.voice_commands_enabled

    return settings

# Search history
@app.post("/search/history")
async def search_history(request: SearchHistoryRequest):
    """Search across all session history"""
    results = []

    for session in session_manager.sessions.values():
        if session.transcriber:
            transcript = session.transcriber.get_transcript()
            if request.query.lower() in transcript.lower():
                results.append({
                    "session_id": session.id,
                    "session_name": session.name,
                    "created_at": session.created_at.isoformat(),
                    "preview": transcript[:200] + "..."
                })

    return {"results": results[:request.limit]}

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)

    try:
        while True:
            await asyncio.sleep(0.5)

            active_session = session_manager.get_session(session_manager.active_session_id) if session_manager.active_session_id else None

            if active_session and active_session.is_running and active_session.transcriber and active_session.responder:
                data = {
                    "type": "update",
                    "session_id": active_session.id,
                    "transcript": active_session.transcriber.get_transcript(),
                    "response": str(active_session.responder.response),
                    "research_status": active_session.responder.get_research_status(),
                    "sources": [s.to_dict() for s in active_session.responder.sources],
                }

                insights = active_session.responder.action_tracker.conversation_insights
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
        websocket_clients.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in websocket_clients:
            websocket_clients.remove(websocket)

if __name__ == "__main__":
    print("Starting Ecoute Enhanced API Server...")
    print("Server running on http://127.0.0.1:8000")
    print("Features: Multi-session, Export, Search, Voice Commands, Integrations")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
