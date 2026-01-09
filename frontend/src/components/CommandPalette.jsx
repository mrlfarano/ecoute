import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search, FileDown, Mail, Settings, History,
  Plus, Sparkles, Command, ChevronRight
} from 'lucide-react';

function CommandPalette({ isOpen, onClose, onCommand }) {
  const [search, setSearch] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  const commands = [
    {
      id: 'new-session',
      name: 'New Session',
      icon: Plus,
      shortcut: 'Cmd+N',
      action: 'newSession',
      keywords: ['create', 'start', 'begin']
    },
    {
      id: 'export-markdown',
      name: 'Export as Markdown',
      icon: FileDown,
      action: 'export',
      params: { format: 'markdown' },
      keywords: ['download', 'save', 'md']
    },
    {
      id: 'export-json',
      name: 'Export as JSON',
      icon: FileDown,
      action: 'export',
      params: { format: 'json' },
      keywords: ['download', 'save']
    },
    {
      id: 'export-html',
      name: 'Export as HTML',
      icon: FileDown,
      action: 'export',
      params: { format: 'html' },
      keywords: ['download', 'save', 'web']
    },
    {
      id: 'email-draft',
      name: 'Generate Email Draft',
      icon: Mail,
      action: 'emailDraft',
      keywords: ['compose', 'write', 'follow-up']
    },
    {
      id: 'search-history',
      name: 'Search History',
      icon: History,
      shortcut: 'Cmd+F',
      action: 'searchHistory',
      keywords: ['find', 'past', 'previous']
    },
    {
      id: 'settings',
      name: 'Settings',
      icon: Settings,
      shortcut: 'Cmd+,',
      action: 'settings',
      keywords: ['preferences', 'config', 'options']
    },
    {
      id: 'deep-dive',
      name: 'Deep Dive Research...',
      icon: Sparkles,
      shortcut: 'Cmd+D',
      action: 'deepDive',
      keywords: ['research', 'explore', 'investigate']
    }
  ];

  const filteredCommands = commands.filter(cmd => {
    const searchLower = search.toLowerCase();
    return (
      cmd.name.toLowerCase().includes(searchLower) ||
      cmd.keywords?.some(k => k.includes(searchLower))
    );
  });

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
      setSearch('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(i => (i + 1) % filteredCommands.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(i => (i - 1 + filteredCommands.length) % filteredCommands.length);
      } else if (e.key === 'Enter' && filteredCommands[selectedIndex]) {
        e.preventDefault();
        executeCommand(filteredCommands[selectedIndex]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, filteredCommands]);

  const executeCommand = (cmd) => {
    if (onCommand) {
      onCommand(cmd.action, cmd.params);
    }
    onClose();
    setSearch('');
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-start justify-center pt-32"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: -20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: -20 }}
          className="w-full max-w-2xl bg-discord-dark rounded-lg shadow-2xl border border-discord-gray overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Search Input */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-discord-gray">
            <Search className="w-5 h-5 text-discord-text-muted" />
            <input
              ref={inputRef}
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Type a command or search..."
              className="flex-1 bg-transparent text-discord-text placeholder-discord-text-muted outline-none text-lg"
            />
            <div className="flex items-center gap-1 text-xs text-discord-text-muted">
              <Command className="w-3 h-3" />
              <span>K</span>
            </div>
          </div>

          {/* Commands List */}
          <div className="max-h-96 overflow-y-auto">
            {filteredCommands.length === 0 ? (
              <div className="px-4 py-8 text-center text-discord-text-muted">
                No commands found
              </div>
            ) : (
              <div className="py-2">
                {filteredCommands.map((cmd, index) => {
                  const Icon = cmd.icon;
                  return (
                    <button
                      key={cmd.id}
                      onClick={() => executeCommand(cmd)}
                      onMouseEnter={() => setSelectedIndex(index)}
                      className={`
                        w-full px-4 py-3 flex items-center gap-3 transition-colors
                        ${index === selectedIndex
                          ? 'bg-discord-accent text-white'
                          : 'text-discord-text hover:bg-discord-gray-light'
                        }
                      `}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="flex-1 text-left font-medium">{cmd.name}</span>
                      {cmd.shortcut && (
                        <span className="text-xs opacity-60">{cmd.shortcut}</span>
                      )}
                      <ChevronRight className="w-4 h-4 opacity-60" />
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="px-4 py-2 border-t border-discord-gray bg-discord-darker">
            <div className="flex items-center gap-4 text-xs text-discord-text-muted">
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-discord-gray rounded">↑↓</kbd>
                Navigate
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-discord-gray rounded">Enter</kbd>
                Select
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-discord-gray rounded">Esc</kbd>
                Close
              </span>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default CommandPalette;
