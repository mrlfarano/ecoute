import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, X, Radio } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function SessionTabs({ activeSessionId, onSessionChange, onNewSession }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creatingSession, setCreatingSession] = useState(false);

  useEffect(() => {
    loadSessions();
    const interval = setInterval(loadSessions, 5000); // Refresh every 5s
    return () => clearInterval(interval);
  }, []);

  const loadSessions = async () => {
    try {
      const response = await axios.get(`${API_URL}/sessions`);
      setSessions(response.data.sessions || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load sessions:', error);
      setLoading(false);
    }
  };

  const createSession = async () => {
    setCreatingSession(true);
    try {
      const sessionName = `Session ${new Date().toLocaleTimeString()}`;
      const response = await axios.post(`${API_URL}/sessions`, {
        name: sessionName,
        use_api: true,
        enable_search: true
      });

      const newSessionId = response.data.session_id;
      await loadSessions();

      if (onNewSession) {
        onNewSession(newSessionId);
      }
    } catch (error) {
      console.error('Failed to create session:', error);
    } finally {
      setCreatingSession(false);
    }
  };

  const deleteSession = async (sessionId, e) => {
    e.stopPropagation();

    if (sessions.length <= 1) {
      alert('Cannot delete the last session');
      return;
    }

    try {
      await axios.delete(`${API_URL}/sessions/${sessionId}`);
      await loadSessions();

      // If deleted session was active, switch to first available
      if (activeSessionId === sessionId && sessions.length > 1) {
        const nextSession = sessions.find(s => s.id !== sessionId);
        if (nextSession && onSessionChange) {
          onSessionChange(nextSession.id);
        }
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const activateSession = async (sessionId) => {
    try {
      await axios.post(`${API_URL}/sessions/${sessionId}/activate`);
      if (onSessionChange) {
        onSessionChange(sessionId);
      }
    } catch (error) {
      console.error('Failed to activate session:', error);
    }
  };

  if (loading) {
    return (
      <div className="h-12 bg-discord-dark border-b border-discord-gray flex items-center px-4">
        <div className="text-discord-text-muted text-sm">Loading sessions...</div>
      </div>
    );
  }

  return (
    <div className="h-12 bg-discord-dark border-b border-discord-gray flex items-center px-2 overflow-x-auto">
      <div className="flex items-center gap-1 min-w-0">
        <AnimatePresence mode="popLayout">
          {sessions.map((session) => (
            <motion.div
              key={session.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="relative group"
            >
              <button
                onClick={() => activateSession(session.id)}
                className={`
                  px-4 py-2 rounded-t transition-colors flex items-center gap-2 min-w-0
                  ${session.is_active || session.id === activeSessionId
                    ? 'bg-discord-darkest text-discord-text border-t-2 border-discord-accent'
                    : 'bg-discord-gray text-discord-text-muted hover:bg-discord-gray-light'
                  }
                `}
              >
                {session.is_running && (
                  <Radio className="w-3 h-3 text-discord-green animate-pulse" />
                )}
                <span className="text-sm font-medium truncate max-w-[150px]">
                  {session.name}
                </span>

                {sessions.length > 1 && (
                  <button
                    onClick={(e) => deleteSession(session.id, e)}
                    className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-discord-red/20 rounded p-0.5"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </button>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* New Session Button */}
        <button
          onClick={createSession}
          disabled={creatingSession}
          className="px-3 py-2 bg-discord-gray hover:bg-discord-gray-light text-discord-text-muted hover:text-discord-text rounded transition-colors flex items-center gap-1 ml-2"
          title="New Session (Cmd+N)"
        >
          <Plus className="w-4 h-4" />
          {creatingSession ? (
            <span className="text-xs">Creating...</span>
          ) : (
            <span className="text-xs">New</span>
          )}
        </button>
      </div>
    </div>
  );
}

export default SessionTabs;
