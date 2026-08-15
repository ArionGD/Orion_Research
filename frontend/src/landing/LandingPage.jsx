import React from 'react';
import { 
  ShieldCheck, 
  Activity, 
  TrendingUp, 
  Moon, 
  Cpu, 
  ArrowRight, 
  Lock, 
  Sparkles,
  Zap,
  Globe2,
  Database
} from 'lucide-react';

export default function LandingPage({ onOpenLogin, onLaunchGuest }) {
  return (
    <div className="min-h-screen bg-[#080b11] text-slate-100 flex flex-col font-sans selection:bg-amber-500/20 selection:text-amber-400">
      {/* Top Header Navbar */}
      <header className="border-b border-slate-800/80 bg-[#0d121c]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 via-amber-600 to-purple-600 flex items-center justify-center text-black font-bold text-xl shadow-lg shadow-amber-500/10">
              Ω
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight bg-gradient-to-r from-slate-100 via-slate-200 to-slate-400 bg-clip-text text-transparent">
                ORION RESEARCH
              </span>
              <span className="block text-[10px] font-mono text-amber-500 font-semibold tracking-wider">
                ACE v5.5 + VED ENGINE
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              GCP CLOUD RUN ACTIVE
            </div>
            
            <button
              onClick={onOpenLogin}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-semibold text-sm transition-all shadow-lg shadow-amber-500/20 flex items-center gap-2 cursor-pointer active:scale-95"
            >
              <Lock className="w-4 h-4" />
              Superuser Login
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-6 overflow-hidden">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-tr from-amber-500/10 via-purple-600/10 to-blue-600/10 blur-[120px] pointer-events-none rounded-full" />
        
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/90 border border-amber-500/30 text-amber-400 text-xs font-mono mb-8 shadow-inner">
            <Sparkles className="w-4 h-4" />
            <span>Mundane Astrological Intelligence & Geopolitical Risk Core</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight leading-tight text-white mb-6">
            Predictive Risk Gravity & <br />
            <span className="bg-gradient-to-r from-amber-400 via-amber-300 to-purple-400 bg-clip-text text-transparent">
              Vedic Financial Intelligence
            </span>
          </h1>

          <p className="text-slate-400 text-base md:text-lg max-w-3xl mx-auto mb-10 leading-relaxed font-light">
            Combining the high-performance ACE v5 Medini Sovereign Malefic Index (SMI) with 596+ astronomical algorithms from the official VedAstro Jyotish Engine.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
            <button
              onClick={onOpenLogin}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm transition-all shadow-xl shadow-amber-500/25 flex items-center justify-center gap-3 cursor-pointer"
            >
              <span>Access Research Terminal</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="py-16 px-6 max-w-7xl mx-auto w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl bg-[#0e131f] border border-slate-800/80 hover:border-amber-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-6 group-hover:scale-110 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 mb-3">Sovereign Malefic Index</h3>
            <p className="text-slate-400 text-sm leading-relaxed font-light">
              Real-time multi-planetary malefic aspect scoring (SMI) evaluating systemic market risk gravity and volatility peaks.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-[#0e131f] border border-slate-800/80 hover:border-purple-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-6 group-hover:scale-110 transition-transform">
              <Moon className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 mb-3">Official VedAstro Engine</h3>
            <p className="text-slate-400 text-sm leading-relaxed font-light">
              Direct Python backend integration (`ved_engine`) calculating Panchanga, Vimshottari Dasa, and Divisional charts (D1-D60).
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-[#0e131f] border border-slate-800/80 hover:border-blue-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform">
              <TrendingUp className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 mb-3">Commodity ML Models</h3>
            <p className="text-slate-400 text-sm leading-relaxed font-light">
              Explainable Boosting Machines (EBM) and Neural ANOVA models predicting Gold, Silver, and XLE Energy spikes.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800/80 py-8 px-6 bg-[#0b0e17]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500 font-mono">
          <div>© 2026 ORION RESEARCH & MEDINI ENGINE. ALL RIGHTS RESERVED.</div>
          <div className="flex items-center gap-6">
            <span>FastAPI Backend v5.5.0</span>
            <span>VedAstro Jyotish Library v1.23</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
