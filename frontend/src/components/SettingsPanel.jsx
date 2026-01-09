import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Save, Key, Palette, Zap, Bell, Keyboard } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function SettingsPanel({ isOpen, onClose }) {
  const [settings, setSettings] = useState({
    theme: 'discord-dark',
    llm_provider: 'openai',
    notification_enabled: true,
    voice_commands_enabled: false
  });
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    try {
      const response = await axios.get(`${API_URL}/settings`);
      setSettings(response.data);
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.post(`${API_URL}/settings`, {
        ...settings,
        ...(apiKey ? { api_key: apiKey } : {})
      });

      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const themes = [
    { id: 'discord-dark', name: 'Discord Dark', preview: '#1e1f22' },
    { id: 'light', name: 'Light', preview: '#ffffff' },
    { id: 'solarized', name: 'Solarized Dark', preview: '#002b36' },
    { id: 'dracula', name: 'Dracula', preview: '#282a36' }
  ];

  const llmProviders = [
    { id: 'openai', name: 'OpenAI (GPT-4, GPT-4o-mini)' },
    { id: 'anthropic', name: 'Anthropic (Claude Opus, Sonnet)' },
    { id: 'local', name: 'Local Model (Llama, Mistral)' }
  ];

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-2xl bg-discord-dark rounded-lg shadow-2xl border border-discord-gray overflow-hidden max-h-[90vh] flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-discord-gray flex-shrink-0">
            <div>
              <h2 className="text-xl font-bold text-discord-text">Settings</h2>
              <p className="text-sm text-discord-text-muted mt-1">
                Customize your Ecoute experience
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-discord-gray rounded transition-colors"
            >
              <X className="w-5 h-5 text-discord-text-muted" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-6 space-y-6">
              {/* API Key */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Key className="w-5 h-5 text-discord-accent" />
                  <h3 className="text-lg font-semibold text-discord-text">API Key</h3>
                </div>
                <p className="text-sm text-discord-text-muted mb-3">
                  OpenAI API key for transcription and AI responses
                </p>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full px-4 py-2 bg-discord-gray-light border border-discord-gray-lighter rounded text-discord-text placeholder-discord-text-muted focus:outline-none focus:border-discord-accent"
                />
                <p className="text-xs text-discord-text-muted mt-2">
                  Leave blank to keep current key
                </p>
              </div>

              {/* Theme */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Palette className="w-5 h-5 text-discord-accent" />
                  <h3 className="text-lg font-semibold text-discord-text">Theme</h3>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {themes.map((theme) => (
                    <button
                      key={theme.id}
                      onClick={() => setSettings({ ...settings, theme: theme.id })}
                      className={`
                        p-4 rounded-lg border-2 transition-all flex items-center gap-3
                        ${settings.theme === theme.id
                          ? 'border-discord-accent bg-discord-accent/10'
                          : 'border-discord-gray bg-discord-gray-light hover:border-discord-gray-lighter'
                        }
                      `}
                    >
                      <div
                        className="w-8 h-8 rounded border-2 border-discord-gray-lighter"
                        style={{ backgroundColor: theme.preview }}
                      />
                      <span className="text-discord-text font-medium">{theme.name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* LLM Provider */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Zap className="w-5 h-5 text-discord-accent" />
                  <h3 className="text-lg font-semibold text-discord-text">AI Provider</h3>
                </div>
                <p className="text-sm text-discord-text-muted mb-3">
                  Choose which AI model provider to use
                </p>
                <div className="space-y-2">
                  {llmProviders.map((provider) => (
                    <label
                      key={provider.id}
                      className={`
                        flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors
                        ${settings.llm_provider === provider.id
                          ? 'bg-discord-accent/20 border border-discord-accent'
                          : 'bg-discord-gray-light hover:bg-discord-gray border border-transparent'
                        }
                      `}
                    >
                      <input
                        type="radio"
                        name="llm_provider"
                        checked={settings.llm_provider === provider.id}
                        onChange={() => setSettings({ ...settings, llm_provider: provider.id })}
                        className="w-4 h-4 accent-discord-accent"
                      />
                      <span className="text-discord-text">{provider.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Notifications */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Bell className="w-5 h-5 text-discord-accent" />
                  <h3 className="text-lg font-semibold text-discord-text">Notifications</h3>
                </div>
                <label className="flex items-center justify-between p-4 rounded-lg bg-discord-gray-light hover:bg-discord-gray cursor-pointer transition-colors">
                  <div>
                    <p className="text-discord-text font-medium">Enable Notifications</p>
                    <p className="text-sm text-discord-text-muted mt-1">
                      Get notified about action items and important events
                    </p>
                  </div>
                  <input
                    type="checkbox"
                    checked={settings.notification_enabled}
                    onChange={(e) => setSettings({ ...settings, notification_enabled: e.target.checked })}
                    className="w-5 h-5 rounded accent-discord-accent"
                  />
                </label>
              </div>

              {/* Voice Commands */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Keyboard className="w-5 h-5 text-discord-accent" />
                  <h3 className="text-lg font-semibold text-discord-text">Voice Commands</h3>
                </div>
                <label className="flex items-center justify-between p-4 rounded-lg bg-discord-gray-light hover:bg-discord-gray cursor-pointer transition-colors">
                  <div>
                    <p className="text-discord-text font-medium">Enable Voice Commands</p>
                    <p className="text-sm text-discord-text-muted mt-1">
                      Control Ecoute with voice (e.g., "Ecoute, research...")
                    </p>
                  </div>
                  <input
                    type="checkbox"
                    checked={settings.voice_commands_enabled}
                    onChange={(e) => setSettings({ ...settings, voice_commands_enabled: e.target.checked })}
                    className="w-5 h-5 rounded accent-discord-accent"
                  />
                </label>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-discord-gray flex items-center justify-between flex-shrink-0">
            <div className="text-xs text-discord-text-muted">
              Version 3.0.0 • Ecoute AI Research Assistant
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-discord-text-muted hover:text-discord-text transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-6 py-2 bg-discord-accent hover:bg-discord-accent-hover text-white rounded transition-colors flex items-center gap-2 disabled:opacity-50"
              >
                {saving ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Saving...
                  </>
                ) : saved ? (
                  <>
                    <Save className="w-4 h-4" />
                    Saved!
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    Save
                  </>
                )}
              </button>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default SettingsPanel;
