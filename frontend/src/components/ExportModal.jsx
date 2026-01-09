import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Download, Copy, FileText, Code, Globe, Check } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function ExportModal({ isOpen, onClose, sessionId }) {
  const [format, setFormat] = useState('markdown');
  const [includeTranscript, setIncludeTranscript] = useState(true);
  const [includeSources, setIncludeSources] = useState(true);
  const [includeInsights, setIncludeInsights] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);
  const [exportedContent, setExportedContent] = useState('');
  const [copied, setCopied] = useState(false);

  const formats = [
    { id: 'markdown', name: 'Markdown', icon: FileText, extension: '.md' },
    { id: 'json', name: 'JSON', icon: Code, extension: '.json' },
    { id: 'html', name: 'HTML', icon: Globe, extension: '.html' }
  ];

  const handleExport = async () => {
    if (!sessionId) return;

    setExporting(true);
    try {
      const response = await axios.post(`${API_URL}/export`, {
        session_id: sessionId,
        format: format,
        include_transcript: includeTranscript,
        include_sources: includeSources,
        include_insights: includeInsights
      });

      setExportedContent(response.data.content);
      setExported(true);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    } finally {
      setExporting(false);
    }
  };

  const handleDownload = () => {
    const selectedFormat = formats.find(f => f.id === format);
    const blob = new Blob([exportedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ecoute-export-${Date.now()}${selectedFormat.extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(exportedContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Copy failed:', error);
    }
  };

  const handleClose = () => {
    setExported(false);
    setExportedContent('');
    setCopied(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={handleClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-3xl bg-discord-dark rounded-lg shadow-2xl border border-discord-gray overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-discord-gray">
            <div>
              <h2 className="text-xl font-bold text-discord-text">Export Session</h2>
              <p className="text-sm text-discord-text-muted mt-1">
                {exported ? 'Export complete!' : 'Choose format and options'}
              </p>
            </div>
            <button
              onClick={handleClose}
              className="p-2 hover:bg-discord-gray rounded transition-colors"
            >
              <X className="w-5 h-5 text-discord-text-muted" />
            </button>
          </div>

          {!exported ? (
            <>
              {/* Format Selection */}
              <div className="px-6 py-4">
                <label className="block text-sm font-medium text-discord-text mb-3">
                  Format
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {formats.map((fmt) => {
                    const Icon = fmt.icon;
                    return (
                      <button
                        key={fmt.id}
                        onClick={() => setFormat(fmt.id)}
                        className={`
                          p-4 rounded-lg border-2 transition-all flex flex-col items-center gap-2
                          ${format === fmt.id
                            ? 'border-discord-accent bg-discord-accent/10 text-discord-accent'
                            : 'border-discord-gray bg-discord-gray-light text-discord-text hover:border-discord-gray-lighter'
                          }
                        `}
                      >
                        <Icon className="w-6 h-6" />
                        <span className="font-medium">{fmt.name}</span>
                        <span className="text-xs opacity-60">{fmt.extension}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Options */}
              <div className="px-6 py-4 border-t border-discord-gray">
                <label className="block text-sm font-medium text-discord-text mb-3">
                  Include
                </label>
                <div className="space-y-2">
                  {[
                    { key: 'transcript', label: 'Transcript', state: includeTranscript, setState: setIncludeTranscript },
                    { key: 'sources', label: 'Sources & Citations', state: includeSources, setState: setIncludeSources },
                    { key: 'insights', label: 'Insights & Action Items', state: includeInsights, setState: setIncludeInsights }
                  ].map(({ key, label, state, setState }) => (
                    <label
                      key={key}
                      className="flex items-center gap-3 p-3 rounded-lg bg-discord-gray-light hover:bg-discord-gray cursor-pointer transition-colors"
                    >
                      <input
                        type="checkbox"
                        checked={state}
                        onChange={(e) => setState(e.target.checked)}
                        className="w-4 h-4 rounded border-discord-gray-lighter bg-discord-gray accent-discord-accent"
                      />
                      <span className="text-discord-text">{label}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="px-6 py-4 border-t border-discord-gray flex items-center justify-end gap-3">
                <button
                  onClick={handleClose}
                  className="px-4 py-2 text-discord-text-muted hover:text-discord-text transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleExport}
                  disabled={exporting}
                  className="px-6 py-2 bg-discord-accent hover:bg-discord-accent-hover text-white rounded transition-colors flex items-center gap-2 disabled:opacity-50"
                >
                  {exporting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Exporting...
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" />
                      Export
                    </>
                  )}
                </button>
              </div>
            </>
          ) : (
            <>
              {/* Preview */}
              <div className="px-6 py-4">
                <label className="block text-sm font-medium text-discord-text mb-3">
                  Preview
                </label>
                <div className="bg-discord-darkest rounded-lg p-4 max-h-96 overflow-auto">
                  <pre className="text-sm text-discord-text whitespace-pre-wrap font-mono">
                    {exportedContent.substring(0, 1000)}
                    {exportedContent.length > 1000 && '\n\n... (truncated)'}
                  </pre>
                </div>
              </div>

              {/* Actions */}
              <div className="px-6 py-4 border-t border-discord-gray flex items-center justify-end gap-3">
                <button
                  onClick={handleCopy}
                  className="px-4 py-2 bg-discord-gray hover:bg-discord-gray-light text-discord-text rounded transition-colors flex items-center gap-2"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4 text-discord-green" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copy
                    </>
                  )}
                </button>
                <button
                  onClick={handleDownload}
                  className="px-6 py-2 bg-discord-accent hover:bg-discord-accent-hover text-white rounded transition-colors flex items-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  Download
                </button>
              </div>
            </>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default ExportModal;
