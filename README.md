# 🎧 Ecoute - AI Research Assistant

**Ecoute** is a powerful AI-powered desktop application for real-time transcription, intelligent research, and conversation insights. Built with modern web technologies for a beautiful, Discord-style experience.

---

## ✨ Key Features

- 🎤 **Real-time transcription** - Live audio from mic and speakers
- 🤖 **AI response suggestions** - Powered by GPT-4o-mini
- 🔍 **Intelligent research** - Automatic web search with source citations
- 📊 **Conversation insights** - Action items, key topics, and decisions
- 🎨 **Beautiful UI** - Modern, Discord-inspired interface
- ⚡ **Fast & responsive** - Built with Electron and React
- 🌐 **Cross-platform** - Windows, macOS, and Linux

---

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+**
- **FFmpeg** (for audio processing)
- **OpenAI API key**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mrlfarano/ecoute
   cd ecoute
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node dependencies:**
   ```bash
   npm install
   cd frontend && npm install && cd ..
   ```

4. **Set up your OpenAI API key:**

   Create `backend/keys.py`:
   ```python
   OPENAI_API_KEY = "your-api-key-here"
   ```

### Running the App

```bash
npm start
```

This starts:
- Python FastAPI backend
- React development server
- Electron window

The app will open automatically!

---

## 📖 Documentation

- **[ELECTRON_README.md](ELECTRON_README.md)** - Complete Electron app guide
- **[FEATURES.md](FEATURES.md)** - Detailed feature documentation
- **[BUILD.md](BUILD.md)** - Building and packaging instructions
- **[README_CLASSIC.md](README_CLASSIC.md)** - Original tkinter version docs

---

## 🎨 UI Preview

```
┌──────────────────────────────────────────────────────────┐
│  🎧 Ecoute AI      ● Connected    [Start] [Clear] ⚙️    │
├──────────────────────────────────────────────────────────┤
│ 🎤 Transcript  │ 🔍 Research    │ 📊 Insights           │
│ ─────────────  │ ──────────     │ ─────────             │
│ Live audio...  │ • Searching... │ ⚡ Key Topics         │
│                │ 📖 Sources     │ ✅ Decisions          │
│ ✨ AI Response │ [1] Source 1   │ ⏰ Action Items       │
└────────────────┴────────────────┴───────────────────────┘
```

---

## 🏗️ Architecture

**Modern Stack:**
- ⚡ **Electron** - Desktop framework
- ⚛️ **React 18** - UI framework
- 🎨 **Tailwind CSS** - Styling
- 🐍 **FastAPI** - Python backend
- 🔌 **WebSocket** - Real-time updates

**Project Structure:**
```
ecoute/
├── electron/        # Electron main process
├── frontend/        # React UI
├── backend/         # Python FastAPI server
└── package.json     # Build configuration
```

---

## 📦 Building

### Development
```bash
npm start
```

### Production Build
```bash
npm run package
```

Creates installers for:
- **Windows**: `.exe` installer
- **macOS**: `.dmg` image
- **Linux**: `.AppImage`

See [ELECTRON_README.md](ELECTRON_README.md) for detailed build instructions.

---

## 🎯 Use Cases

- **Meetings** - Auto-track action items and decisions
- **Research** - Get cited sources in real-time
- **Interviews** - Never miss important points
- **Learning** - Deep dive into any topic
- **Collaboration** - Stay on top of conversations

---

## 🆚 Versions

### Electron App (Current)
- ✅ Modern, beautiful UI
- ✅ Discord-style design
- ✅ Real-time WebSocket updates
- ✅ System tray integration
- ✅ Professional installers

### Classic (tkinter)
- See [README_CLASSIC.md](README_CLASSIC.md) and `main.py`
- Simple but functional
- Good for Python-only environments

**We recommend the Electron version for the best experience!**

---

## 🔧 Requirements

### System Requirements
- **Windows 10+** / **macOS 10.13+** / **Ubuntu 18.04+**
- **4GB RAM** minimum (8GB recommended)
- **Microphone** and **speakers**
- **Internet connection** for AI features

### API Requirements
- **OpenAI API key** with GPT-4o-mini access
- Recommended: Whisper API enabled (--api flag)

---

## 📝 Configuration

### API Key Setup

**Option 1:** Create `backend/keys.py`
```python
OPENAI_API_KEY = "sk-..."
```

**Option 2:** Environment variable
```bash
export OPENAI_API_KEY="sk-..."
```

### FFmpeg Installation

**Windows:**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
pip install -r requirements.txt
```

### Frontend errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Audio not working
- Check microphone/speaker permissions
- Verify FFmpeg is installed
- Check default audio devices in system settings

See [ELECTRON_README.md](ELECTRON_README.md) for more troubleshooting.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Electron](https://www.electronjs.org/), [React](https://react.dev/), and [FastAPI](https://fastapi.tiangolo.com/)
- UI inspired by [Discord](https://discord.com/)
- Powered by [OpenAI](https://openai.com/)

---

## 🔗 Links

- **GitHub**: [github.com/mrlfarano/ecoute](https://github.com/mrlfarano/ecoute)
- **Issues**: [Report bugs or request features](https://github.com/mrlfarano/ecoute/issues)
- **Discussions**: [Join the community](https://github.com/mrlfarano/ecoute/discussions)

---

**Made with ❤️ to be your #1 work tool**

Start using Ecoute today and transform how you handle conversations!
