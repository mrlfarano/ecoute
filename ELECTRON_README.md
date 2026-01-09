# 🚀 Ecoute Electron - Modern Desktop App

Welcome to the **Electron version** of Ecoute! This is a complete rewrite using modern web technologies to create a beautiful, Discord-style desktop application.

---

## 🎨 What's New?

### Modern Tech Stack
- ⚡ **Electron** - Cross-platform desktop framework
- ⚛️ **React 18** - Modern, fast UI framework
- 🎨 **Tailwind CSS** - Beautiful, utility-first styling
- 🐍 **FastAPI** - High-performance Python backend
- 🔌 **WebSocket** - Real-time updates
- ✨ **Framer Motion** - Smooth animations

### Beautiful UI
- 🌑 **Discord-inspired dark theme**
- 💫 **Smooth animations and transitions**
- 📱 **Responsive layout**
- 🎯 **Clean, modern design**
- ⚡ **Hardware-accelerated rendering**

### New Features
- 🔔 **System tray integration**
- 🔄 **Real-time WebSocket updates**
- 💾 **Persistent settings**
- 🔥 **Hot reload in development**
- 📦 **Professional installers**

---

## 📁 Project Structure

```
ecoute/
├── electron/                 # Electron main process
│   ├── main.js              # Main Electron entry point
│   └── preload.js           # Preload script for security
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Tailwind styles
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── backend/                  # Python FastAPI backend
│   ├── api_server.py        # FastAPI REST API & WebSocket
│   ├── AudioTranscriber.py  # Audio processing
│   ├── GPTResponder.py      # AI responses
│   ├── SearchEngine.py      # Web search
│   └── ActionTracker.py     # Insights tracking
│
└── package.json              # Root Electron config
```

---

## 🚀 Getting Started

### Prerequisites

1. **Node.js 18+** and npm
2. **Python 3.8+**
3. **FFmpeg** installed on your system

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node dependencies:**
   ```bash
   # Root (Electron)
   npm install

   # Frontend (React)
   cd frontend
   npm install
   cd ..
   ```

3. **Set up your OpenAI API key:**
   Create `backend/keys.py`:
   ```python
   OPENAI_API_KEY = "your-api-key-here"
   ```

   Or set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Running in Development

**Option 1: All at once (recommended)**
```bash
npm start
```

This starts:
- Python backend on `http://127.0.0.1:8000`
- React frontend on `http://localhost:3000`
- Electron window

**Option 2: Manual start**
```bash
# Terminal 1 - Backend
python backend/api_server.py

# Terminal 2 - Frontend
cd frontend && npm start

# Terminal 3 - Electron
npm run start:electron
```

---

## 🎨 UI Overview

### Discord-Style Layout

```
┌────────────────────────────────────────────────────────────────┐
│  🎧 Ecoute AI          ● Connected      [Start] [Clear] ⚙️    │
├────────────────────────────────────────────────────────────────┤
│                    │                    │                       │
│  🎤 Live Transcript │ 🔍 Research       │ 📊 Insights          │
│                    │   Activity         │                       │
│  [transcript       │                    │  ⚡ Key Topics        │
│   content here]    │  ⏳ Currently:     │  • Topic 1           │
│                    │    → Query 1       │  • Topic 2           │
│                    │                    │                       │
│                    │  📚 Recent:        │  ✅ Decisions        │
│ ───────────────    │    • Search 1      │  • Decision 1        │
│                    │    • Search 2      │                       │
│  ✨ AI Suggestion  │                    │  ⏰ Action Items     │
│                    │  📖 Sources        │  🔴 High priority    │
│  [AI response]     │  [1] Source 1      │  🟡 Medium           │
│                    │  [2] Source 2      │                       │
│                    │                    │                       │
└────────────────────┴────────────────────┴───────────────────────┘
```

### Color Scheme

- **Background**: Dark grays (#1e1f22, #111214)
- **Accents**: Discord blue (#5865f2)
- **Status**: Green (active), Yellow (warning), Red (error)
- **Text**: Light gray (#dbdee1) with muted variants

---

## 🏗️ Building for Production

### Build the Frontend
```bash
cd frontend
npm run build
cd ..
```

### Package for All Platforms
```bash
npm run package
```

### Platform-Specific Builds

**Windows:**
```bash
npm run build:win
```
Creates: `dist-electron/Ecoute Setup.exe`

**macOS:**
```bash
npm run build:mac
```
Creates: `dist-electron/Ecoute.dmg`

**Linux:**
```bash
npm run build:linux
```
Creates: `dist-electron/Ecoute.AppImage`

---

## 🔧 Architecture

### Communication Flow

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│   Electron  │         │    React     │         │    Python    │
│   (Main)    │ ◄─IPC──► │  (Renderer)  │ ◄─HTTP──► │   FastAPI    │
│             │         │              │  WebSocket │              │
│  • Window   │         │  • UI        │         │  • Audio      │
│  • Tray     │         │  • State     │         │  • AI         │
│  • Startup  │         │  • Display   │         │  • Search     │
└─────────────┘         └──────────────┘         └──────────────┘
```

### Key Technologies

**Frontend:**
- React 18 with Hooks
- Tailwind CSS for styling
- Framer Motion for animations
- Axios for HTTP requests
- WebSocket for real-time updates

**Backend:**
- FastAPI for REST API
- Uvicorn ASGI server
- WebSocket for live updates
- All existing Python AI logic

**Electron:**
- Main process for window management
- Preload script for security
- IPC for inter-process communication
- electron-store for settings persistence

---

## 🎯 Features

### Implemented

✅ Real-time transcription display
✅ AI-generated response suggestions
✅ Live research activity monitoring
✅ Source citations display
✅ Conversation insights and action items
✅ WebSocket for instant updates
✅ System tray integration
✅ Modern, Discord-style UI
✅ Cross-platform support

### Coming Soon

🔜 Deep dive research window
🔜 Settings panel
🔜 Keyboard shortcuts
🔜 Auto-updates
🔜 Multiple conversation sessions
🔜 Export functionality
🔜 Custom themes
🔜 Plugin system

---

## ⚙️ Configuration

### Electron Settings

Stored in `electron-store`:
- API keys (encrypted)
- User preferences
- Window position/size
- Theme settings

Access via:
```javascript
window.electronAPI.getStoreValue('key')
window.electronAPI.setStoreValue('key', value)
```

### Backend Configuration

Edit `backend/api_server.py` for:
- Port number (default: 8000)
- CORS settings
- WebSocket update interval
- Logging level

---

## 🐛 Troubleshooting

### Backend won't start
**Issue:** `ModuleNotFoundError: No module named 'fastapi'`
**Solution:** `pip install -r requirements.txt`

### Frontend won't connect
**Issue:** WebSocket connection failed
**Solution:** Ensure backend is running on port 8000

### Electron window is blank
**Issue:** React build not found
**Solution:** Run `cd frontend && npm run build`

### Audio not working
**Issue:** No microphone/speaker access
**Solution:**
- Windows: Check Privacy & Security settings
- macOS: System Preferences > Security & Privacy
- Linux: Check PulseAudio/ALSA configuration

### Build fails
**Issue:** electron-builder errors
**Solution:**
- Clean node_modules: `rm -rf node_modules && npm install`
- Update electron-builder: `npm install electron-builder@latest --save-dev`

---

## 📚 API Endpoints

### REST API

**Start Session**
```http
POST /session/start
Content-Type: application/json

{
  "use_api": true,
  "enable_search": true
}
```

**Get Transcript**
```http
GET /transcript
```

**Get Response**
```http
GET /response
```

**Get Insights**
```http
GET /insights
```

**Clear Context**
```http
POST /clear
```

### WebSocket

**Connect:**
```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws');
```

**Receive Updates:**
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle real-time updates
};
```

---

## 🎨 Customization

### Changing Colors

Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  discord: {
    accent: '#your-color-here',
    // ... other colors
  }
}
```

### Window Size

Edit `electron/main.js`:
```javascript
mainWindow = new BrowserWindow({
  width: 1600,  // Change width
  height: 900,  // Change height
  // ...
});
```

### Adding Features

1. **Backend:** Add endpoint in `backend/api_server.py`
2. **Frontend:** Create component in `frontend/src/components/`
3. **Integration:** Call API from React component

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

Built with:
- [Electron](https://www.electronjs.org/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Framer Motion](https://www.framer.com/motion/)

Inspired by Discord's beautiful UI/UX design.

---

**Made with ❤️ for the next generation of AI-powered productivity tools**
