import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Mic, Radio, Search, Sparkles, ChevronDown, Settings,
  Zap, BookOpen, TrendingUp, CheckCircle, Clock, AlertCircle
} from 'lucide-react';
import './index.css';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [researchStatus, setResearchStatus] = useState({});
  const [sources, setSources] = useState([]);
  const [insights, setInsights] = useState({});
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://127.0.0.1:8000/ws');

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'update') {
          setTranscript(data.transcript);
          setResponse(data.response);
          setResearchStatus(data.research_status);
          setSources(data.sources || []);
          setInsights(data.insights || {});
        }
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      wsRef.current = ws;
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const startSession = async () => {
    try {
      const response = await fetch(`${API_URL}/session/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ use_api: true, enable_search: true })
      });
      const data = await response.json();
      if (data.status === 'started' || data.status === 'already_running') {
        setIsRunning(true);
      }
    } catch (error) {
      console.error('Failed to start session:', error);
    }
  };

  const stopSession = async () => {
    try {
      await fetch(`${API_URL}/session/stop`, { method: 'POST' });
      setIsRunning(false);
    } catch (error) {
      console.error('Failed to stop session:', error);
    }
  };

  const clearContext = async () => {
    try {
      await fetch(`${API_URL}/clear`, { method: 'POST' });
      setTranscript('');
      setResponse('');
      setSources([]);
      setInsights({});
    } catch (error) {
      console.error('Failed to clear context:', error);
    }
  };

  return (
    <div className="h-screen bg-discord-darkest flex flex-col overflow-hidden">
      {/* Title Bar */}
      <div className="h-12 bg-discord-dark border-b border-discord-gray flex items-center justify-between px-4 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-discord-accent to-purple-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-discord-text font-bold text-lg">Ecoute AI</h1>
          {connected && (
            <div className="flex items-center gap-2 text-xs text-discord-green">
              <div className="w-2 h-2 rounded-full bg-discord-green animate-pulse"></div>
              Connected
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          {!isRunning ? (
            <button
              onClick={startSession}
              className="px-4 py-1.5 bg-discord-green hover:bg-green-600 text-white rounded transition-colors flex items-center gap-2"
            >
              <Radio className="w-4 h-4" />
              Start Session
            </button>
          ) : (
            <button
              onClick={stopSession}
              className="px-4 py-1.5 bg-discord-red hover:bg-red-600 text-white rounded transition-colors"
            >
              Stop
            </button>
          )}
          <button
            onClick={clearContext}
            className="px-4 py-1.5 bg-discord-gray hover:bg-discord-gray-light text-discord-text rounded transition-colors"
          >
            Clear
          </button>
          <button className="p-2 hover:bg-discord-gray rounded transition-colors">
            <Settings className="w-5 h-5 text-discord-text-muted" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Transcript & Response */}
        <div className="flex-1 flex flex-col p-4 gap-4 overflow-hidden">
          {/* Transcript */}
          <div className="flex-1 bg-discord-dark rounded-lg p-4 overflow-y-auto">
            <div className="flex items-center gap-2 mb-3">
              <Mic className="w-5 h-5 text-discord-accent" />
              <h2 className="text-discord-text font-semibold">Live Transcript</h2>
              {isRunning && (
                <div className="ml-auto">
                  <div className="flex gap-1">
                    <div className="w-1 h-4 bg-discord-accent rounded animate-pulse"></div>
                    <div className="w-1 h-4 bg-discord-accent rounded animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-1 h-4 bg-discord-accent rounded animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              )}
            </div>
            <div className="text-discord-text whitespace-pre-wrap">
              {transcript || (
                <span className="text-discord-text-muted italic">
                  No active transcription. Start a session to begin.
                </span>
              )}
            </div>
          </div>

          {/* AI Response */}
          <div className="h-48 bg-discord-dark rounded-lg p-4 overflow-y-auto border-2 border-discord-green/30">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-discord-green" />
              <h2 className="text-discord-text font-semibold">AI Suggestion</h2>
            </div>
            <div className="text-discord-green text-lg">
              {response || (
                <span className="text-discord-text-muted italic text-base">
                  Waiting for conversation...
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Middle Panel - Research */}
        <div className="w-96 flex flex-col p-4 gap-4 border-l border-r border-discord-gray overflow-hidden">
          {/* Research Activity */}
          <div className="flex-1 bg-discord-dark rounded-lg p-4 overflow-y-auto">
            <div className="flex items-center gap-2 mb-3">
              <Search className="w-5 h-5 text-blue-400" />
              <h2 className="text-discord-text font-semibold">Research Activity</h2>
            </div>

            {researchStatus.active_searches?.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-discord-text-muted mb-2">Currently Researching:</div>
                {researchStatus.active_searches.map((query, i) => (
                  <div key={i} className="flex items-center gap-2 text-sm text-blue-400 mb-1">
                    <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
                    {query}
                  </div>
                ))}
              </div>
            )}

            {researchStatus.recent_searches?.length > 0 && (
              <div>
                <div className="text-xs text-discord-text-muted mb-2">Recent Searches:</div>
                {researchStatus.recent_searches.map((query, i) => (
                  <div key={i} className="text-sm text-discord-text-muted mb-1">
                    • {query}
                  </div>
                ))}
              </div>
            )}

            {(!researchStatus.active_searches || researchStatus.active_searches.length === 0) &&
             (!researchStatus.recent_searches || researchStatus.recent_searches.length === 0) && (
              <div className="text-discord-text-muted italic text-sm">
                No active research
              </div>
            )}
          </div>

          {/* Sources */}
          <div className="flex-1 bg-discord-dark rounded-lg p-4 overflow-y-auto">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="w-5 h-5 text-yellow-400" />
              <h2 className="text-discord-text font-semibold">Sources</h2>
              {sources.length > 0 && (
                <span className="ml-auto text-xs text-discord-text-muted">{sources.length}</span>
              )}
            </div>

            {sources.length > 0 ? (
              <div className="space-y-3">
                {sources.map((source, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-discord-gray-light rounded p-3"
                  >
                    <div className="text-sm text-yellow-400 font-medium mb-1">
                      [{i + 1}] {source.title}
                    </div>
                    <div className="text-xs text-discord-text-muted line-clamp-2">
                      {source.snippet}
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-discord-text-muted italic text-sm">
                No sources yet
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Insights */}
        <div className="w-96 flex flex-col p-4 gap-4 overflow-hidden">
          <div className="flex-1 bg-discord-dark rounded-lg p-4 overflow-y-auto">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-orange-400" />
              <h2 className="text-discord-text font-semibold">Insights</h2>
            </div>

            {/* Key Topics */}
            {insights.key_topics?.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-discord-text-muted mb-2 flex items-center gap-1">
                  <Zap className="w-3 h-3" />
                  Key Topics
                </div>
                <div className="space-y-1">
                  {insights.key_topics.map((topic, i) => (
                    <div key={i} className="text-sm text-discord-text bg-discord-gray-light rounded px-2 py-1">
                      • {topic}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Decisions */}
            {insights.decisions_made?.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-discord-text-muted mb-2 flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" />
                  Decisions Made
                </div>
                <div className="space-y-1">
                  {insights.decisions_made.map((decision, i) => (
                    <div key={i} className="text-sm text-discord-text">
                      • {decision}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Questions */}
            {insights.questions_raised?.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-discord-text-muted mb-2 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  Open Questions
                </div>
                <div className="space-y-1">
                  {insights.questions_raised.map((question, i) => (
                    <div key={i} className="text-sm text-discord-text">
                      • {question}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Action Items */}
            {insights.action_items?.length > 0 && (
              <div>
                <div className="text-xs text-discord-text-muted mb-2 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  Action Items
                </div>
                <div className="space-y-2">
                  {insights.action_items.map((item, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className={`p-2 rounded ${
                        item.priority === 'high'
                          ? 'bg-red-900/30 border-l-2 border-red-500'
                          : item.priority === 'medium'
                          ? 'bg-yellow-900/30 border-l-2 border-yellow-500'
                          : 'bg-green-900/30 border-l-2 border-green-500'
                      }`}
                    >
                      <div className="text-sm text-discord-text">{item.text}</div>
                      <div className="text-xs text-discord-text-muted mt-1">
                        {item.assigned_to} • {item.priority}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {(!insights.key_topics || insights.key_topics.length === 0) &&
             (!insights.action_items || insights.action_items.length === 0) && (
              <div className="text-discord-text-muted italic text-sm">
                Start a conversation to see insights
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
