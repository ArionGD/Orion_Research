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
  ShieldAlert,
  BarChart3,
  Zap,
  Cpu
} from 'lucide-react';

// Streamed Typewriter Component matching Gemini's signature top-to-bottom text reveal
function StreamedText({ fullText, onUpdate }) {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    let index = 0;
    setDisplayedText('');
    setIsTyping(true);

    const speed = 10; // ms per tick
    const chunkSize = 4; // characters per tick for smooth natural streaming

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
    <div className="whitespace-pre-wrap font-sans text-xs leading-relaxed text-slate-200 transition-all duration-300">
      {displayedText}
      {isTyping && (
        <span className="inline-block w-2 h-4 ml-1 bg-amber-400 animate-pulse rounded-sm align-middle shadow-sm shadow-amber-400" />
      )}
    </div>
  );
}

export default function MudraAIChatPanel() {
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || inputMsg;
    if (!query.trim()) return;

    const userMessage = { id: Date.now(), sender: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);
    setInputMsg('');
    setLoading(true);

    // Construct conversational history array
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
          history: historyPayload 
        })
      });

      if (res.ok) {
        const data = await res.json();
        const aiMessage = {
          id: Date.now() + 1,
          sender: 'ai',
          text: data.reply,
          metrics: data.metrics,
          symbol: data.symbol,
          company_name: data.company_name,
          engine: data.engine
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'ai',
          text: '⚠️ Engine Communication Error. Please check FastAPI backend connection.'
        }]);
      }
    } catch (err) {
      console.error('Error sending chat message:', err);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'ai',
        text: '⚠️ Network connection error.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestionChips = [
    { label: 'Analyze Reliance (RELIANCE) 2-Month Forecast', icon: TrendingUp },
    { label: 'Evaluate State Bank of India (SBIN) Dual Risk', icon: Building2 },
    { label: 'What is TCS & Infosys (INFY) Transit Outlook?', icon: Cpu },
    { label: 'Show Gold (XAU) & Silver 2-Week Dip Probability', icon: Coins }
  ];

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col justify-between bg-[#080b11] rounded-2xl border border-slate-800/90 shadow-2xl relative overflow-hidden font-sans">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-gradient-to-b from-purple-600/10 via-amber-500/5 to-transparent blur-[120px] pointer-events-none" />

      {/* Top Header Bar (Google Gemini Inspired) */}
      <div className="p-4 px-6 border-b border-slate-800/80 bg-[#0e131f]/90 backdrop-blur-md flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-400 via-amber-500 to-purple-600 flex items-center justify-center text-black font-bold shadow-lg shadow-amber-500/20">
            ✦
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-extrabold text-white tracking-tight">Mudra AI</span>
              <span className="px-2 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-[10px] font-mono font-semibold">
                ✦ Gemini 2.5 Flash Connected
              </span>
            </div>
            <span className="text-[11px] text-slate-400 font-light block">
              Agentic Astrological Intelligence & Market Analyst
            </span>
          </div>
        </div>

        {/* Reset Chat Button */}
        <button
          onClick={() => setMessages([])}
          className="px-3.5 py-1.5 rounded-xl bg-[#141a28] hover:bg-slate-800 border border-slate-700/80 text-slate-400 hover:text-slate-200 text-xs font-mono transition-all cursor-pointer"
        >
          Reset Chat
        </button>
      </div>

      {/* Main Chat Conversation Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 z-10">
        {/* Welcome Screen when Empty */}
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto space-y-8 py-12">
            <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-amber-500/20 via-purple-500/20 to-blue-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 text-3xl shadow-2xl animate-pulse">
              ✦
            </div>

            <div className="space-y-2">
              <h2 className="text-3xl font-extrabold text-white tracking-tight">
                Hello, Superuser.
              </h2>
              <p className="text-slate-400 text-sm font-light leading-relaxed">
                Where should Mudra AI focus today? Ask about any NSE Stock, Index, Commodity, or Sovereign SMI Weather risk pattern.
              </p>
            </div>

            {/* Suggestion Chips */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
              {suggestionChips.map((chip, idx) => {
                const Icon = chip.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => handleSend(chip.label)}
                    className="p-4 rounded-2xl bg-[#0e131f] hover:bg-[#141a28] border border-slate-800 hover:border-amber-500/40 text-slate-300 hover:text-amber-300 text-xs font-medium transition-all flex items-center gap-3 cursor-pointer group shadow-lg"
                  >
                    <div className="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0 group-hover:scale-110 transition-transform">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="flex-1 leading-snug">{chip.label}</span>
                    <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 shrink-0" />
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
            className={`flex items-start gap-4 animate-gemini-reveal ${
              msg.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.sender === 'ai' && (
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-400 to-purple-600 flex items-center justify-center text-black font-bold text-sm shrink-0 shadow-lg mt-1">
                ✦
              </div>
            )}

            <div
              className={`max-w-3xl rounded-2xl p-5 text-sm leading-relaxed ${
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

                  {/* Optional Telemetry Metrics Pill Bar */}
                  {msg.metrics && (
                    <div className="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-800/80 font-mono text-xs">
                      <div className="flex items-center gap-2">
                        <span className="px-3 py-1 rounded-lg bg-[#141a28] border border-slate-700 text-amber-400">
                          SMI: {msg.metrics.smi_score}
                        </span>
                        <span className="px-3 py-1 rounded-lg bg-[#141a28] border border-slate-700 text-purple-400">
                          Micro: {msg.metrics.micro_risk}
                        </span>
                        <span className="px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 font-bold">
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
              <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-amber-400 font-mono text-xs shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {/* Loading Indicator */}
        {loading && (
          <div className="flex items-start gap-4 animate-gemini-reveal">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-400 to-purple-600 flex items-center justify-center text-black font-bold text-sm shrink-0 shadow-lg animate-pulse">
              ✦
            </div>
            <div className="p-4 rounded-2xl bg-[#0e131f] border border-slate-800 text-slate-400 text-xs font-mono flex items-center gap-3">
              <RefreshCw className="w-4 h-4 animate-spin text-amber-400" />
              <span>Mudra AI analyzing horoscopes, transits & Gemini Flash model...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Bottom Floating Prompt Bar */}
      <div className="p-4 border-t border-slate-800/80 bg-[#0e131f]/90 backdrop-blur-md z-10">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative max-w-4xl mx-auto flex items-center gap-3"
        >
          <input
            type="text"
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            placeholder="Ask Mudra AI about ANY stock (e.g. TCS, INFY, SBIN, ICICIBANK, Gold, Silver)..."
            className="w-full bg-[#141a28] border border-slate-700/80 focus:border-amber-500 text-white placeholder-slate-500 text-xs font-mono px-5 py-3.5 rounded-2xl outline-none transition-all shadow-inner"
          />

          <button
            type="submit"
            disabled={!inputMsg.trim() || loading}
            className={`px-5 py-3.5 rounded-2xl font-mono text-xs font-bold flex items-center gap-2 transition-all cursor-pointer shrink-0 ${
              inputMsg.trim() && !loading
                ? 'bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 shadow-lg shadow-amber-500/20 hover:scale-105'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>Ask Mudra</span>
          </button>
        </form>
      </div>
    </div>
  );
}
