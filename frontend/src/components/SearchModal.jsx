import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Search, Calendar, FileText, ChevronRight } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function SearchModal({ isOpen, onClose, onSelectSession }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);
  const searchTimeout = useRef(null);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
      setQuery('');
      setResults([]);
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    if (query.length >= 2) {
      // Debounce search
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }

      searchTimeout.current = setTimeout(() => {
        performSearch();
      }, 300);
    } else {
      setResults([]);
    }

    return () => {
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }
    };
  }, [query]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(i => (i + 1) % results.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(i => (i - 1 + results.length) % results.length);
      } else if (e.key === 'Enter' && results[selectedIndex]) {
        e.preventDefault();
        selectSession(results[selectedIndex]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, results]);

  const performSearch = async () => {
    setSearching(true);
    try {
      const response = await axios.post(`${API_URL}/search/history`, {
        query: query,
        limit: 20
      });

      setResults(response.data.results || []);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setSearching(false);
    }
  };

  const selectSession = (result) => {
    if (onSelectSession) {
      onSelectSession(result.session_id);
    }
    onClose();
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  const highlightMatch = (text, query) => {
    if (!query) return text;

    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, i) =>
      part.toLowerCase() === query.toLowerCase() ? (
        <mark key={i} className="bg-discord-accent/30 text-discord-accent rounded px-0.5">
          {part}
        </mark>
      ) : (
        part
      )
    );
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
          className="w-full max-w-3xl bg-discord-dark rounded-lg shadow-2xl border border-discord-gray overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Search Input */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-discord-gray">
            <Search className={`w-5 h-5 ${searching ? 'animate-pulse text-discord-accent' : 'text-discord-text-muted'}`} />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search conversation history..."
              className="flex-1 bg-transparent text-discord-text placeholder-discord-text-muted outline-none text-lg"
            />
            {query && (
              <button
                onClick={() => setQuery('')}
                className="p-1 hover:bg-discord-gray rounded transition-colors"
              >
                <X className="w-4 h-4 text-discord-text-muted" />
              </button>
            )}
          </div>

          {/* Results */}
          <div className="max-h-96 overflow-y-auto">
            {query.length < 2 ? (
              <div className="px-4 py-12 text-center">
                <Search className="w-12 h-12 text-discord-text-muted mx-auto mb-3" />
                <p className="text-discord-text-muted">
                  Type at least 2 characters to search
                </p>
              </div>
            ) : searching ? (
              <div className="px-4 py-12 text-center">
                <div className="w-8 h-8 border-2 border-discord-accent/30 border-t-discord-accent rounded-full animate-spin mx-auto mb-3" />
                <p className="text-discord-text-muted">Searching...</p>
              </div>
            ) : results.length === 0 ? (
              <div className="px-4 py-12 text-center">
                <FileText className="w-12 h-12 text-discord-text-muted mx-auto mb-3" />
                <p className="text-discord-text-muted">No results found</p>
                <p className="text-sm text-discord-text-muted mt-1">
                  Try a different search term
                </p>
              </div>
            ) : (
              <div className="py-2">
                {results.map((result, index) => (
                  <button
                    key={result.session_id}
                    onClick={() => selectSession(result)}
                    onMouseEnter={() => setSelectedIndex(index)}
                    className={`
                      w-full px-4 py-4 flex flex-col gap-2 transition-colors text-left
                      ${index === selectedIndex
                        ? 'bg-discord-accent/10 border-l-2 border-discord-accent'
                        : 'hover:bg-discord-gray-light border-l-2 border-transparent'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-discord-text flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        {result.session_name}
                      </h3>
                      <span className="flex items-center gap-1 text-xs text-discord-text-muted">
                        <Calendar className="w-3 h-3" />
                        {formatDate(result.created_at)}
                      </span>
                    </div>
                    <p className="text-sm text-discord-text-muted line-clamp-2">
                      {highlightMatch(result.preview, query)}
                    </p>
                    <div className="flex items-center gap-2 text-xs text-discord-accent">
                      <span>Open session</span>
                      <ChevronRight className="w-3 h-3" />
                    </div>
                  </button>
                ))}
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
                Open
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-discord-gray rounded">Esc</kbd>
                Close
              </span>
              <span className="ml-auto text-discord-text-muted">
                {results.length} {results.length === 1 ? 'result' : 'results'}
              </span>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default SearchModal;
