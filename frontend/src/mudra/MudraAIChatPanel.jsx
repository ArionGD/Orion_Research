import React, { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  Bot, 
  User, 
  TrendingUp, 
  Building2, 
  Coins, 
  RefreshCw, 
  ChevronRight, 
  BarChart3,
  Cpu,
  History,
  Plus,
  Trash2,
  X,
  MessageSquare,
  PanelRight,
  PanelRightClose
} from 'lucide-react';

// Rich Document & Colorful Markdown Parser for Mudra AI Responses
function renderFormattedContent(text) {
  if (!text) return null;

  const lines = text.split('\n');
  return lines.map((line, lIdx) => {
    const trimmed = line.trim();
    if (!trimmed) return <div key={lIdx} className="h-2" />;

    // 1. Major Section Header (### or **1. ...**)
    if (trimmed.startsWith('###') || trimmed.match(/^\*\*\d+\./) || trimmed.startsWith('####')) {
      const headerText = trimmed.replace(/^###\s*/, '').replace(/^####\s*/, '').replace(/^\*\*/, '').replace(/\*\*:?$/, '');
      return (
        <div key={lIdx} className="my-3 pt-2 pb-1 border-b border-slate-800/80 flex items-center gap-2.5">
          <span className="w-2.5 h-6 rounded-r bg-gradient-to-b from-amber-400 to-purple-500 shadow-md shadow-amber-400/20" />
          <h3 className="text-sm font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-purple-300 tracking-wide uppercase font-mono">
            {headerText}
          </h3>
        </div>
      );
    }

    // 2. Bullet Card / List Item (* or -)
    if (trimmed.startsWith('* ') || trimmed.startsWith('- ') || trimmed.match(/^\*\s+\*\*/)) {
      const content = trimmed.replace(/^[\*\-]\s+/, '');
      return (
        <div key={lIdx} className="my-1.5 ml-2 pl-3 border-l-2 border-amber-500/40 bg-[#0b0e17]/60 hover:bg-[#0f1422] p-2.5 rounded-r-xl transition-all border border-r border-t border-b border-slate-800/60 shadow-sm flex items-start gap-2.5">
          <span className="text-amber-400 text-xs mt-0.5 shrink-0">✦</span>
          <div className="flex-1 leading-relaxed text-xs text-slate-200">
            {parseInlineStyles(content)}
          </div>
        </div>
      );
    }

    // 3. Regular Paragraph
    return (
      <p key={lIdx} className="my-1.5 leading-relaxed text-xs text-slate-300">
        {parseInlineStyles(trimmed)}
      </p>
    );
  });
}

// Inline Style Parser for **bold**, `code`, and colorful metrics
function parseInlineStyles(str) {
  if (!str) return str;
  
  const codeParts = str.split(/(`[^`]+`)/g);
  return codeParts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) {
      const code = part.slice(1, -1);
      return (
        <span key={i} className="mx-1 px-2 py-0.5 rounded-md bg-[#090d16] text-emerald-300 font-mono text-[11px] border border-emerald-500/30 shadow-inner inline-block">
          {code}
        </span>
      );
    }

    const boldParts = part.split(/(\*\*[^*]+\*\*)/g);
    return boldParts.map((bPart, j) => {
      if (bPart.startsWith('**') && bPart.endsWith('**')) {
        const bText = bPart.slice(2, -2);
        
        if (bText.includes('SMI') || bText.includes('7.8') || bText.includes('STORM')) {
          return (
            <span key={j} className="mx-0.5 px-1.5 py-0.5 rounded bg-red-500/15 text-red-300 font-bold border border-red-500/30 text-[11px]">
              {bText}
            </span>
          );
        }
        if (bText.includes('Jupiter') || bText.includes('Saturn') || bText.includes('Rahu') || bText.includes('Eclipse')) {
          return (
            <span key={j} className="mx-0.5 px-1.5 py-0.5 rounded bg-purple-500/15 text-purple-300 font-bold border border-purple-500/30 text-[11px]">
              {bText}
            </span>
          );
        }

        return (
          <strong key={j} className="font-extrabold text-amber-300 bg-amber-500/10 px-1 py-0.5 rounded border border-amber-500/20 shadow-sm">
            {bText}
          </strong>
        );
      }
      return bPart;
    });
  });
}

// Streamed Typewriter Component matching Gemini's signature top-to-bottom text reveal
function StreamedText({ fullText, onUpdate }) {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    let index = 0;
    setDisplayedText('');
    setIsTyping(true);

    const speed = 8;
    const chunkSize = 6;

    const timer = setInterval(() => {
      index += chunkSize;
      if (index >= fullText.length) {
        setDisplayedText(fullText);
        setIsTyping(false);
        clearInterval(timer);
      } else {
        setDisplayedText(fullText.slice(0, index));
      }
      if (onUpdate) onUpdate();
    }, speed);

    return () => clearInterval(timer);
  }, [fullText]);

  return (
    <div className="font-sans text-xs leading-relaxed text-slate-200 transition-all duration-300 space-y-1">
      {renderFormattedContent(displayedText)}
      {isTyping && (
        <span className="inline-block w-2 h-4 ml-1 bg-amber-400 animate-pulse rounded-sm align-middle shadow-sm shadow-amber-400" />
      )}
    </div>
  );
}

export default function MudraAIChatPanel({ onToggleMobileNav }) {
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(() => {
    return localStorage.getItem('mudra_active_session_id') || `session_${Date.now()}`;
  });
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Fetch list of saved sessions from DB
  const loadSessionsList = async () => {
    try {
      const res = await fetch('/api/v1/chat/sessions');
      if (res.ok) {
        const data = await res.json();
        setSessions(data.sessions || []);
      }
    } catch (err) {
      console.error('Error fetching sessions:', err);
    }
  };

  // Load messages for specific session ID from DB
  const loadSessionMessages = async (sessId) => {
    try {
      setLoading(true);
      const res = await fetch(`/api/v1/chat/sessions/${sessId}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || []);
        setCurrentSessionId(sessId);
        localStorage.setItem('mudra_active_session_id', sessId);
      }
    } catch (err) {
      console.error('Error loading session messages:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create fresh conversation thread
  const startNewChat = () => {
    const newId = `session_${Date.now()}`;
    setCurrentSessionId(newId);
    setMessages([]);
    localStorage.setItem('mudra_active_session_id', newId);
    fetch('/api/v1/chat/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: newId, title: 'New Conversation' })
    }).then(() => loadSessionsList());
  };

  // Delete session from DB
  const deleteSession = async (sessId, e) => {
    e.stopPropagation();
    try {
      const res = await fetch(`/api/v1/chat/sessions/${sessId}`, { method: 'DELETE' });
      if (res.ok) {
        setSessions(prev => prev.filter(s => s.id !== sessId));
        if (currentSessionId === sessId) {
          startNewChat();
        }
      }
    } catch (err) {
      console.error('Error deleting session:', err);
    }
  };

  useEffect(() => {
    loadSessionsList();
    if (currentSessionId) {
      loadSessionMessages(currentSessionId);
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || inputMsg;
    if (!query.trim()) return;

    const userMessage = { id: `user_${Date.now()}`, sender: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);
    setInputMsg('');
    setLoading(true);

    const historyPayload = messages.slice(-6).map(m => ({
      role: m.sender === 'user' ? 'user' : 'model',
      text: m.text
    }));

    try {
      const res = await fetch('/api/v1/chat/mudra', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: query, 
          session_id: currentSessionId,
          history: historyPayload 
        })
      });

      if (res.ok) {
        const data = await res.json();
        const aiMessage = {
          id: `ai_${Date.now()}`,
          sender: 'ai',
          text: data.reply,
          metrics: data.metrics,
          symbol: data.symbol,
          company_name: data.company_name,
          engine: data.engine
        };
        setMessages(prev => [...prev, aiMessage]);
        loadSessionsList(); // Refresh sidebar list
      } else {
        setMessages(prev => [...prev, {
          id: `err_${Date.now()}`,
          sender: 'ai',
          text: '⚠️ Engine Communication Error. Please check FastAPI backend connection.'
        }]);
      }
    } catch (err) {
      console.error('Error sending chat message:', err);
      setMessages(prev => [...prev, {
        id: `err_${Date.now()}`,
        sender: 'ai',
        text: '⚠️ Network connection error.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestionChips = [
    { label: 'Reliance', prompt: 'Analyze Reliance (RELIANCE) 2-Month Forecast', icon: TrendingUp },
    { label: 'SBI Risk', prompt: 'Evaluate State Bank of India (SBIN) Dual Risk', icon: Building2 },
    { label: 'TCS & INFY', prompt: 'What is TCS & Infosys (INFY) Transit Outlook?', icon: Cpu },
    { label: 'Gold & Silver', prompt: 'Show Gold (XAU) & Silver 2-Week Dip Probability', icon: Coins }
  ];

  return (
    <div className="flex-1 h-full flex flex-col justify-between bg-[#080b11] rounded-none sm:rounded-2xl border-0 sm:border border-slate-800/90 shadow-2xl relative overflow-hidden font-sans">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-gradient-to-b from-purple-600/10 via-amber-500/5 to-transparent blur-[120px] pointer-events-none" />

      {/* Top Header Bar */}
      <div className="p-3.5 sm:p-5 px-4 sm:px-6 border-b border-slate-800/80 bg-[#0e131f]/90 backdrop-blur-md flex items-center justify-between z-20">
        <div className="flex items-center gap-3">
          <button
            onClick={() => onToggleMobileNav && onToggleMobileNav()}
            className="flex items-center gap-2.5 cursor-pointer lg:cursor-default group text-left"
            title="Toggle Menu"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-br from-amber-400 via-amber-500 to-purple-600 flex items-center justify-center text-black font-bold text-sm shadow-lg shadow-amber-500/20 group-hover:scale-105 transition-transform">
              ✦
            </div>
            <div>
              <span className="text-sm sm:text-base font-extrabold text-white tracking-tight block">Mudra AI</span>
            </div>
          </button>
        </div>

        {/* Right Header Action Bar (New Chat & Expand/Collapse Chat History Drawer) */}
        <div className="flex items-center gap-2">
          <button
            onClick={startNewChat}
            title="Start New Chat"
            className="p-2 sm:px-3 sm:py-1.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-sm"
          >
            <Plus className="w-4 h-4 sm:w-3.5 sm:h-3.5" />
            <span className="hidden sm:inline">New Chat</span>
          </button>

          <button
            onClick={() => setDrawerOpen(!drawerOpen)}
            title={drawerOpen ? "Collapse Conversations Drawer" : "Expand Chat History Drawer"}
            className="p-2 rounded-xl bg-[#141a28] hover:bg-slate-800 border border-slate-700/80 text-amber-400 transition-all flex items-center gap-2 cursor-pointer shadow-sm"
          >
            {drawerOpen ? <PanelRightClose className="w-4 h-4" /> : <PanelRight className="w-4 h-4" />}
            <span className="text-xs font-mono font-bold hidden sm:inline">
              {drawerOpen ? "Close Drawer" : "Chat History"}
            </span>
          </button>
        </div>
      </div>

      {/* Main Workspace Body with Slide-over Right Drawer */}
      <div className="flex-1 flex relative overflow-hidden z-10">
        {/* Main Chat Conversation Scroll Area */}
        <div className="flex-1 overflow-y-auto p-3 sm:p-6 space-y-4 sm:space-y-6 flex flex-col">
          {/* Welcome Screen when Empty */}
          {messages.length === 0 && (
            <div className="my-auto flex flex-col items-center justify-center text-center max-w-2xl mx-auto space-y-5 sm:space-y-6 py-4 px-2">
              <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-3xl bg-gradient-to-tr from-amber-500/20 via-purple-500/20 to-blue-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 text-2xl sm:text-3xl shadow-2xl animate-pulse">
                ✦
              </div>

              <div className="space-y-2">
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                  Hello, Superuser.
                </h2>
                <p className="text-slate-400 text-xs sm:text-sm font-light leading-relaxed">
                  Where should Mudra AI focus today? Ask about any NSE Stock, Index, Commodity, or Sovereign SMI Weather risk pattern.
                </p>
              </div>

              {/* Suggestion Chips */}
              <div className="grid grid-cols-2 gap-2 w-full text-left max-w-md">
                {suggestionChips.map((chip, idx) => {
                  const Icon = chip.icon;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSend(chip.prompt || chip.label)}
                      className="p-2.5 rounded-xl bg-[#0e131f] hover:bg-[#141a28] border border-slate-800 hover:border-amber-500/40 text-slate-300 hover:text-amber-300 text-xs font-medium transition-all flex items-center justify-between cursor-pointer group shadow-sm"
                    >
                      <div className="flex items-center gap-2">
                        <Icon className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span className="font-mono text-xs font-semibold">{chip.label}</span>
                      </div>
                      <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-400 shrink-0" />
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Conversation Thread */}
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start gap-2.5 sm:gap-4 animate-gemini-reveal ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.sender === 'ai' && (
                <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-gradient-to-br from-amber-400 to-purple-600 flex items-center justify-center text-black font-bold text-xs sm:text-sm shrink-0 shadow-lg mt-1">
                  ✦
                </div>
              )}

              <div
                className={`max-w-[88vw] sm:max-w-3xl rounded-2xl p-3.5 sm:p-5 text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-amber-500/15 border border-amber-500/40 text-white rounded-tr-none font-mono text-xs'
                    : 'bg-[#0e131f] border border-slate-800/90 text-slate-200 rounded-tl-none shadow-xl space-y-4'
                }`}
              >
                {msg.sender === 'user' ? (
                  <span>{msg.text}</span>
                ) : (
                  <div className="space-y-4">
                    {/* Formatted Streamed Reply Body */}
                    <StreamedText fullText={msg.text} onUpdate={scrollToBottom} />

                    {/* Telemetry Metrics Bar */}
                    {msg.metrics && (
                      <div className="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-800/80 font-mono text-xs">
                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-0.5 sm:px-3 sm:py-1 rounded-lg bg-[#141a28] border border-slate-700 text-amber-400 text-[10px] sm:text-xs">
                            SMI: {msg.metrics.smi_score}
                          </span>
                          <span className="px-2.5 py-0.5 sm:px-3 sm:py-1 rounded-lg bg-[#141a28] border border-slate-700 text-purple-400 text-[10px] sm:text-xs">
                            Micro: {msg.metrics.micro_risk}
                          </span>
                          <span className="px-2.5 py-0.5 sm:px-3 sm:py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 font-bold text-[10px] sm:text-xs">
                            Dual Index: {msg.metrics.dual_risk}
                          </span>
                        </div>

                        {msg.engine && (
                          <span className="text-[10px] text-purple-400 font-mono">
                            Powered by {msg.engine}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-amber-400 font-mono text-xs shrink-0 mt-1">
                  <User className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                </div>
              )}
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex items-start gap-3 sm:gap-4 animate-gemini-reveal">
              <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-gradient-to-br from-amber-400 to-purple-600 flex items-center justify-center text-black font-bold text-xs sm:text-sm shrink-0 shadow-lg animate-pulse">
                ✦
              </div>
              <div className="p-3.5 sm:p-4 rounded-2xl bg-[#0e131f] border border-slate-800 text-slate-400 text-xs font-mono flex items-center gap-3">
                <RefreshCw className="w-4 h-4 animate-spin text-amber-400" />
                <span>Mudra AI analyzing horoscopes, transits & Gemini Flash model...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Right Expandable / Collapsible Chat History Sidebar Drawer (Full width on Mobile) */}
        <div
          className={`w-full sm:w-80 bg-[#0c101a] border-l border-slate-800/90 flex flex-col transition-all duration-300 z-30 absolute top-0 right-0 bottom-0 ${
            drawerOpen ? 'translate-x-0 shadow-2xl' : 'translate-x-full pointer-events-none'
          }`}
        >
          {/* Drawer Header */}
          <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-[#0e131f]">
            <div className="flex items-center gap-2 text-slate-200 font-mono text-xs font-bold">
              <History className="w-4 h-4 text-amber-400" />
              <span>Saved Conversations</span>
            </div>
            <button
              onClick={() => setDrawerOpen(false)}
              className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Sessions List */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {sessions.length === 0 ? (
              <div className="text-center text-slate-500 text-xs py-8 font-mono">
                No saved conversations yet.
              </div>
            ) : (
              sessions.map((sess) => {
                const isActive = sess.id === currentSessionId;
                return (
                  <div
                    key={sess.id}
                    onClick={() => loadSessionMessages(sess.id)}
                    className={`p-3 rounded-xl border text-xs cursor-pointer transition-all flex items-start justify-between group ${
                      isActive
                        ? 'bg-amber-500/15 border-amber-500/40 text-amber-300 font-bold shadow-md'
                        : 'bg-[#121724] hover:bg-[#181f30] border-slate-800/80 text-slate-300 hover:text-white'
                    }`}
                  >
                    <div className="flex items-start gap-2.5 overflow-hidden">
                      <MessageSquare className={`w-3.5 h-3.5 mt-0.5 shrink-0 ${isActive ? 'text-amber-400' : 'text-slate-500'}`} />
                      <div className="truncate">
                        <div className="truncate font-mono leading-tight">{sess.title || 'Conversation'}</div>
                        <div className="text-[10px] text-slate-500 font-mono mt-1">
                          {sess.updated_at ? new Date(sess.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={(e) => deleteSession(sess.id, e)}
                      title="Delete thread"
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 text-slate-500 hover:text-red-400 rounded transition-all shrink-0 ml-1"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* Bottom Gemini-Style Unified Single Capsule Input Bar */}
      <div className="shrink-0 p-3 sm:p-4 bg-[#080b11] border-t border-slate-800/80 z-30">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="max-w-4xl mx-auto flex items-center justify-between bg-[#141a28] border border-slate-700/80 focus-within:border-amber-500 rounded-full p-1.5 pl-5 shadow-lg transition-all"
        >
          <input
            type="text"
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            placeholder="Ask Mudra AI (e.g. TCS, INFY, SBIN, Gold)..."
            className="w-full bg-transparent text-white placeholder-slate-500 text-xs font-mono outline-none pr-3"
          />

          <button
            type="submit"
            disabled={!inputMsg.trim() || loading}
            title="Send Message"
            className={`w-9 h-9 rounded-full transition-all cursor-pointer shrink-0 flex items-center justify-center shadow-md ${
              inputMsg.trim() && !loading
                ? 'bg-amber-500 text-slate-950 hover:scale-105 shadow-amber-500/20'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
