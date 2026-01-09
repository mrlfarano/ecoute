# 🤖 CLAUDE.md - Development Context & History

This document provides context for Claude (or any AI assistant) working on this project.

---

## 📋 Project Overview

**Ecoute** - AI-Powered Research and Transcription Assistant

**Current Version:** 3.0.0
**Status:** Production-Ready Backend, Enhanced Frontend
**Last Updated:** 2026-01-09

---

## 🎯 Project Mission

Transform live conversations into actionable intelligence through:
- Real-time transcription (microphone + speakers)
- AI-powered response suggestions
- Intelligent web research with source citations
- Automatic action item tracking
- Conversation insights and analytics
- Professional export capabilities

**Goal:** Be the user's #1 work tool for meetings, research, and conversations.

---

## 🏗️ Architecture

### Stack Overview

```
┌─────────────────────────────────────────────────────┐
│                   Electron App                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   React UI   │◄─┤  Electron    │◄─┤  Python   │ │
│  │  (Frontend)  │  │    (Main)    │  │  FastAPI  │ │
│  │              │  │              │  │  (Backend)│ │
│  │ - Tailwind   │  │ - Window     │  │           │ │
│  │ - Framer     │  │ - Tray       │  │ - Audio   │ │
│  │   Motion     │  │ - IPC        │  │ - AI      │ │
│  │ - WebSocket  │  │ - Storage    │  │ - Search  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────┘
```

### Technology Choices

**Frontend:**
- **React 18** - Modern UI framework with hooks
- **Tailwind CSS** - Utility-first styling (Discord theme)
- **Framer Motion** - Smooth animations
- **Axios** - HTTP client
- **WebSocket** - Real-time updates

**Backend:**
- **FastAPI** - High-performance Python API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Type validation
- **WebSocket** - Real-time communication
- **OpenAI API** - GPT-4o-mini for AI responses
- **Whisper** - Audio transcription (local + API)

**Desktop:**
- **Electron** - Cross-platform desktop framework
- **electron-builder** - Packaging and distribution
- **electron-store** - Settings persistence

**Audio:**
- **PyAudioWPatch** - Audio capture (Windows optimized)
- **FFmpeg** - Audio processing
- **faster-whisper** - Local transcription with GPU support

---

## 📂 Project Structure

```
ecoute/
├── electron/                    # Electron main process
│   ├── main.js                 # Window management, startup
│   └── preload.js              # Secure IPC bridge
│
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.jsx             # Main Discord-style UI
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Tailwind + custom styles
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── tailwind.config.js      # Discord theme colors
│   └── postcss.config.js
│
├── backend/                     # Python FastAPI backend
│   ├── api_server.py           # Main API with 23 endpoints
│   ├── AudioRecorder.py        # Mic/speaker capture
│   ├── AudioTranscriber.py     # Whisper transcription
│   ├── GPTResponder.py         # AI response generation
│   ├── SearchEngine.py         # Web research
│   ├── ActionTracker.py        # Insights extraction
│   ├── DeepDive.py             # Comprehensive research
│   ├── TranscriberModels.py    # Model management
│   ├── prompts.py              # AI prompts
│   └── keys.py                 # API keys (gitignored)
│
├── assets/                      # Icons and images
│   ├── icon.ico                # Windows icon
│   ├── icon.icns               # macOS icon
│   └── icon.png                # Linux icon
│
├── package.json                 # Root Electron config
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── ELECTRON_README.md           # Electron-specific guide
├── FEATURES.md                  # Original features doc
├── FEATURES_V3.md              # V3.0 feature list
├── BUILD.md                     # Build & packaging guide
├── README_CLASSIC.md           # tkinter version docs
└── CLAUDE.md                    # This file
```

---

## 🔄 Development Evolution

### Phase 1: Original (tkinter)
- Simple transcription app
- Basic UI with CustomTkinter
- Single session
- GPT response suggestions
- Limited features

**Files:** `main.py`, basic Python modules

### Phase 2: Research Assistant (Enhanced Python)
- Added SearchEngine for web research
- Source citation tracking
- Action item extraction
- Conversation insights
- Deep dive research
- Three-panel UI

**Key Addition:** Real research with transparency

### Phase 3: Electron Transformation (Current)
- Complete rewrite as Electron app
- React frontend with Discord-style UI
- FastAPI backend with REST + WebSocket
- Real-time updates
- System tray integration
- Professional packaging

**Major Upgrade:** Modern desktop application

### Phase 4: V3.0 Feature Pack (Latest)
- Multi-session management
- Export system (MD/JSON/HTML)
- Email draft generation
- Voice command system
- Smart search across history
- Multi-LLM support
- Settings management
- Integration framework

**Status:** Backend complete, frontend needs UI components

---

## 🎨 Design Philosophy

### UI/UX Principles
1. **Discord-inspired** - Modern, clean, dark theme
2. **Information density** - Show everything relevant
3. **Real-time feedback** - Live updates, no waiting
4. **Transparency** - Show what AI is doing
5. **Keyboard-friendly** - Power user shortcuts
6. **Professional** - Polished, production-quality

### Color Scheme (Discord Theme)
```javascript
discord: {
  dark: '#1e1f22',        // Main background
  darker: '#111214',       // Deeper background
  darkest: '#060607',      // Window background
  gray: '#2b2d31',         // Panel background
  accent: '#5865f2',       // Primary action (blue)
  green: '#23a559',        // Success/active
  yellow: '#f0b232',       // Warning/sources
  red: '#f23f43',          // Error/high priority
  text: '#dbdee1',         // Primary text
  'text-muted': '#949ba4'  // Secondary text
}
```

### Component Layout
```
┌────────────────────────────────────────────────────┐
│  Title Bar (Connection • Actions • Settings)       │
├──────────────┬──────────────┬──────────────────────┤
│ Left Panel   │ Middle Panel │ Right Panel          │
│ (60%)        │ (20%)        │ (20%)                │
│              │              │                      │
│ 🎤 Transcript│ 🔍 Research  │ 📊 Insights          │
│              │              │                      │
│ ✨ Response  │ 📖 Sources   │ Action Items         │
└──────────────┴──────────────┴──────────────────────┘
```

---

## 🔌 API Architecture

### Backend Endpoints (23 total)

#### Core (2)
- `GET /` - API info and feature list
- `GET /status` - System status and active session

#### Sessions (6)
- `POST /sessions` - Create new session
- `GET /sessions` - List all sessions
- `DELETE /sessions/{id}` - Delete session
- `POST /sessions/{id}/start` - Start transcription
- `POST /sessions/{id}/stop` - Stop transcription
- `POST /sessions/{id}/activate` - Set active session

#### Data Retrieval (3)
- `GET /sessions/{id}/transcript` - Get transcript
- `GET /sessions/{id}/response` - Get AI response
- `GET /sessions/{id}/insights` - Get insights/actions

#### Features (7)
- `POST /export` - Export session (MD/JSON/HTML)
- `POST /email/draft` - Generate email draft
- `POST /voice/command` - Process voice command
- `POST /search/history` - Search all sessions
- `GET /settings` - Get current settings
- `POST /settings` - Update settings
- `WS /ws` - WebSocket for real-time updates

#### Research (Existing)
- All SearchEngine endpoints
- Deep dive functionality
- Source tracking

### WebSocket Protocol

**Client → Server:** Connect to `ws://localhost:8000/ws`

**Server → Client (every 500ms):**
```json
{
  "type": "update",
  "session_id": "uuid",
  "transcript": "conversation text...",
  "response": "AI suggestion...",
  "research_status": {
    "active_searches": ["query1"],
    "recent_searches": ["query2", "query3"],
    "total_sources": 5
  },
  "sources": [
    {
      "title": "Source Title",
      "snippet": "Preview text...",
      "url": "https://...",
      "source_type": "web"
    }
  ],
  "insights": {
    "key_topics": ["topic1", "topic2"],
    "decisions_made": ["decision1"],
    "questions_raised": ["question1"],
    "action_items": [
      {
        "text": "Task description",
        "priority": "high",
        "assigned_to": "Person",
        "completed": false
      }
    ]
  }
}
```

---

## 🚀 Feature Status

### ✅ Fully Implemented

**Multi-Session Management**
- Backend: ✅ Complete (SessionManager, 6 endpoints)
- Frontend: ⏳ Needs tab UI

**Export System**
- Backend: ✅ Complete (MD/JSON/HTML generators)
- Frontend: ⏳ Needs export modal

**Email Drafting**
- Backend: ✅ Complete (AI generation)
- Frontend: ⏳ Needs draft modal

**Voice Commands**
- Backend: ✅ Complete (parser + framework)
- Frontend: ⏳ Needs voice UI

**Smart Search**
- Backend: ✅ Complete (full-text search)
- Frontend: ⏳ Needs search modal

**Settings**
- Backend: ✅ Complete (persistence)
- Frontend: ⏳ Needs settings panel

**Multi-LLM**
- Backend: ✅ Complete (provider framework)
- Frontend: ⏳ Needs provider selection

**Real-time Updates**
- Backend: ✅ WebSocket working
- Frontend: ✅ Connected and updating

**Core Features**
- Backend: ✅ All working
- Frontend: ✅ Discord UI complete

---

## 🔑 Key Technologies & Libraries

### Python Backend
```python
fastapi>=0.109.0          # Web framework
uvicorn[standard]>=0.27.0 # ASGI server
websockets>=12.0          # Real-time communication
pydantic>=2.0.0           # Data validation
openai>=1.12.0            # GPT API
faster-whisper            # Local transcription
PyAudioWPatch>=0.2.12.5   # Audio capture
torch>=2.2.0              # GPU acceleration
ctranslate2==3.24.0       # Whisper optimization
numpy>=1.26.0             # Numerical operations
```

### Node.js Frontend
```json
{
  "electron": "^28.0.0",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "tailwindcss": "^3.4.1",
  "framer-motion": "^10.18.0",
  "axios": "^1.6.5",
  "electron-builder": "^24.9.1",
  "electron-store": "^8.1.0"
}
```

---

## 💡 Important Design Decisions

### Why Electron?
- **Cross-platform** - Single codebase for Windows/macOS/Linux
- **Modern UI** - Use web technologies (React, CSS)
- **Auto-updates** - Built-in update system
- **System integration** - Tray, notifications, shortcuts
- **Familiar** - Discord, VS Code, Slack all use it

### Why FastAPI?
- **Fast** - High performance async Python
- **Type-safe** - Pydantic validation
- **Auto-docs** - Swagger UI at `/docs`
- **WebSocket** - Built-in support
- **Modern** - Python 3.8+ features

### Why Multi-Session?
- **Real need** - People have multiple conversations per day
- **Unique** - No other transcription app does this
- **Powerful** - Compare past conversations, track context
- **Professional** - Enterprise-grade feature

### Why WebSocket?
- **Real-time** - Instant updates, no polling
- **Efficient** - Single connection, low overhead
- **Smooth** - Seamless user experience
- **Scalable** - Handles multiple clients

---

## 🐛 Known Limitations

### Current
1. **Windows-focused** - PyAudioWPatch optimized for Windows
2. **In-memory** - Sessions lost on restart (DB coming)
3. **Single user** - No authentication yet
4. **Local only** - No cloud sync (optional future)
5. **English primary** - Multi-language with `--api` flag

### Not Bugs, By Design
1. **Default audio devices** - Security & simplicity
2. **API key required** - OpenAI account needed
3. **Memory usage** - GPU acceleration trades RAM for speed

---

## 🔧 Development Workflow

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
npm install
cd frontend && npm install && cd ..

# Configure API key
echo 'OPENAI_API_KEY="sk-..."' > backend/keys.py

# Run development
npm start
```

### Testing Backend
```bash
# Start server
python backend/api_server.py

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/sessions
```

### Building
```bash
# Build frontend
cd frontend && npm run build && cd ..

# Package app
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

---

## 📊 Performance Characteristics

### Resource Usage
- **CPU**: Moderate (transcription), Low (idle)
- **RAM**: ~500MB base + ~2GB with GPU model
- **GPU**: Optional (CUDA for faster transcription)
- **Network**: API calls only (can run offline with local models)
- **Disk**: Minimal (sessions in memory)

### Latency
- **Transcription**: ~1-3 seconds (local), <1s (API)
- **AI Response**: ~2-5 seconds
- **Research**: ~3-10 seconds per query
- **WebSocket**: <100ms updates
- **Export**: <1 second

---

## 🔐 Security Considerations

### Current Implementation
- ✅ API keys in gitignored files
- ✅ CORS restricted to localhost
- ✅ No sensitive data in logs
- ✅ Electron contextIsolation enabled
- ✅ Input validation (Pydantic)

### Future Enhancements
- 🔜 API key encryption at rest
- 🔜 End-to-end encryption option
- 🔜 User authentication
- 🔜 Audit logging
- 🔜 PII redaction

---

## 🎓 Code Conventions

### Python
- **Style**: PEP 8
- **Type hints**: Where beneficial
- **Docstrings**: For public APIs
- **Async**: Use `async/await` for I/O
- **Error handling**: Specific exceptions

### JavaScript/React
- **Style**: Airbnb-ish
- **Components**: Functional with hooks
- **State**: useState, useEffect
- **Naming**: camelCase (JS), PascalCase (components)
- **CSS**: Tailwind utility classes

### Git Commits
- **Format**: Conventional Commits
- **Scope**: Feature-focused
- **Detail**: What + Why

---

## 📚 Documentation Files

### For Users
- **README.md** - Quick start, main features
- **ELECTRON_README.md** - Electron-specific guide
- **BUILD.md** - Building and packaging
- **FEATURES.md** - Original feature list
- **FEATURES_V3.md** - V3.0 comprehensive features

### For Developers
- **CLAUDE.md** - This file (AI context)
- **API docs** - Auto-generated at `/docs`
- **Code comments** - Inline documentation
- **Type hints** - Self-documenting APIs

---

## 🚦 Current Development Status

### What's Working ✅
- Electron app launches
- React UI renders
- FastAPI backend runs
- WebSocket connects
- Audio recording works
- Transcription works (local + API)
- AI responses generate
- Research searches work
- Sources display
- Insights extract
- Action items track
- Multi-session backend
- Export system
- Email drafting
- Voice commands
- Smart search
- Settings management

### What's Pending ⏳
- Session tabs UI
- Export modal
- Email draft modal
- Settings panel UI
- Search modal UI
- Command palette (Cmd+K)
- Keyboard shortcuts
- Theme picker
- Notification system
- Integration connectors

### What's Next 🔮
- Database persistence
- Cloud sync (optional)
- Mobile companion app
- Calendar integration
- Task management sync
- Advanced analytics
- Custom AI personas
- Plugin system

---

## 💼 Business Context

### Target Users
- **Knowledge workers** - Meetings, research
- **Consultants** - Client conversations
- **Researchers** - Interviews, analysis
- **Students** - Lectures, study groups
- **Journalists** - Interviews, fact-checking
- **Sales** - Customer calls, notes

### Use Cases
1. **Meetings** - Auto-track action items
2. **Interviews** - Never miss important points
3. **Research** - Get cited sources instantly
4. **Learning** - Deep dive any topic
5. **Sales calls** - Follow-up email drafts
6. **Brainstorming** - Capture and organize ideas

### Competitive Advantage
- ✅ Multi-session (unique)
- ✅ Real research with sources
- ✅ Action item extraction
- ✅ Export flexibility
- ✅ LLM agnostic
- ✅ Beautiful UI
- ✅ Local + cloud options
- ✅ Open source

---

## 🎯 Future Roadmap

### Short Term (Next Sprint)
1. Complete frontend UI components
2. Session tabs
3. Export/settings modals
4. Keyboard shortcuts
5. Polish animations

### Medium Term (Next Month)
1. Database persistence (SQLite)
2. Calendar integration
3. Task management sync
4. Advanced theming
5. Mobile app prototype

### Long Term (Next Quarter)
1. Cloud sync (optional)
2. Team collaboration
3. Plugin system
4. Advanced analytics
5. Enterprise features

---

## 🤝 Contribution Guidelines

### For AI Assistants
1. **Read this file** - Understand context
2. **Check status** - Know what's done
3. **Follow conventions** - Match existing code
4. **Test changes** - Ensure nothing breaks
5. **Document** - Update relevant docs
6. **Commit properly** - Clear, detailed messages

### Key Points
- Backend is production-ready
- Frontend needs UI components
- All features have backend support
- API is well-documented
- Code is type-safe where possible
- UI matches Discord theme

---

## 📞 Quick Reference

### Start Development
```bash
npm start
```

### Test API
```bash
curl http://localhost:8000/docs
```

### Build
```bash
npm run package
```

### Branches
- `main` - Stable release
- `claude/project-overview-D3BUL` - Current development

### Ports
- **3000** - React dev server
- **8000** - FastAPI backend

### Important Files
- `backend/api_server.py` - Main API (600+ lines)
- `frontend/src/App.jsx` - Main UI
- `electron/main.js` - Electron setup
- `package.json` - Build config

---

## 🎉 Summary

**Ecoute V3.0** is a production-ready, feature-rich AI research assistant with:
- 23 API endpoints
- Multi-session support
- Export system
- Email generation
- Voice commands
- Smart search
- Beautiful Electron UI
- Real-time updates

**Backend:** Complete and tested
**Frontend:** Base UI working, advanced modals pending
**Status:** Ready for final UI polish and distribution

---

**Last Updated:** 2026-01-09
**Maintainer:** Claude (AI Assistant)
**Version:** 3.0.0-beta

---

*This file helps AI assistants understand the project context, architecture, status, and best practices. Keep it updated as the project evolves.*
