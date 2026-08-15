import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  AlertTriangle, 
  Sparkles, 
  ShieldAlert, 
  TrendingUp, 
  Calendar, 
  MapPin, 
  Activity,
  Layers,
  ChevronRight,
  Cpu,
  Landmark,
  Zap,
  BarChart3,
  Search
} from 'lucide-react';

export default function CompanyAnalysisPanel({ currentSmi = 5.5 }) {
  const [selectedSymbol, setSelectedSymbol] = useState('NIFTY50');
  const [incorporationDate, setIncorporationDate] = useState('1996-04-22');
  const [companyName, setCompanyName] = useState('Nifty 50 Index');
  const [presetCompanies, setPresetCompanies] = useState({});
  const [analysisData, setAnalysisData] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPresets();
  }, []);

  useEffect(() => {
    fetchCompanyAnalysis(selectedSymbol, incorporationDate);
  }, [selectedSymbol, currentSmi]);

  const fetchPresets = async () => {
    try {
      const res = await fetch('/api/v1/company/presets');
      if (res.ok) {
        const data = await res.json();
        setPresetCompanies(data.companies || {});
      }
    } catch (err) {
      console.error('Error fetching presets:', err);
    }
  };

  const fetchCompanyAnalysis = async (symbol, incDate) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/company/analysis?symbol=${symbol}&incorporation_date=${incDate}&smi=${currentSmi}`);
      if (res.ok) {
        const data = await res.json();
        setAnalysisData(data);
      }
    } catch (err) {
      console.error('Error fetching company analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPreset = (symbol) => {
    setSelectedSymbol(symbol);
    const preset = presetCompanies[symbol];
    if (preset) {
      setIncorporationDate(preset.date);
      setCompanyName(preset.name);
      fetchCompanyAnalysis(symbol, preset.date);
    }
  };

  const categories = ['All', 'Indices & ETFs', 'BFSI', 'IT', 'Energy & Power'];

  const filteredSymbols = Object.keys(presetCompanies).filter(sym => {
    if (selectedCategory === 'All') return true;
    return presetCompanies[sym]?.category === selectedCategory;
  });

  return (
    <div className="space-y-8">
      {/* Top Header Card */}
      <div className="p-8 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-xl relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600/10 blur-[100px] rounded-full pointer-events-none" />

        <div className="relative z-10 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-mono mb-3">
                <Building2 className="w-3.5 h-3.5" />
                <span>NSE Stocks & Indices Dual Risk Evaluator</span>
              </div>
              <h2 className="text-2xl font-extrabold text-white tracking-tight">
                Corporate Natal Chart & Disaster Recipe Engine
              </h2>
              <p className="text-slate-400 text-xs mt-1 font-light max-w-2xl">
                Calculates the alignment between **Macro Mundane SMI Weather** and **NSE Stock Inception / Incorporation Horoscopes**.
              </p>
            </div>

            {/* Category Filter Pills */}
            <div className="flex flex-wrap items-center gap-2 bg-[#141a28] p-1.5 rounded-xl border border-slate-700/80">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all cursor-pointer ${
                    selectedCategory === cat
                      ? 'bg-purple-600 text-white shadow-md shadow-purple-600/20'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {/* Preset Stock Tickers Bar */}
          <div className="space-y-2 pt-2 border-t border-slate-800/60">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Select Ticker / Index:
            </span>
            <div className="flex flex-wrap gap-2">
              {filteredSymbols.map(sym => {
                const isSelected = selectedSymbol === sym;
                return (
                  <button
                    key={sym}
                    onClick={() => handleSelectPreset(sym)}
                    className={`px-3.5 py-2 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-amber-500 text-black shadow-lg shadow-amber-500/20'
                        : 'bg-[#141a28] border border-slate-700/80 text-slate-300 hover:border-slate-500'
                    }`}
                  >
                    {sym}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Main Dual Alignment Matrix Grid */}
      {analysisData && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Box 1: Mundane Macro Risk */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <div className="text-xs uppercase font-medium text-slate-400 tracking-wider flex items-center justify-between">
              <span>Mundane Sector SMI (Macro)</span>
              <Activity className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-bold font-mono text-amber-400 my-3">
              {analysisData.mundane_smi_score.toFixed(2)}
            </div>
            <p className="text-xs text-slate-400 leading-relaxed font-light">
              Macro astrological volatility acting on the {analysisData.sector} sector.
            </p>
          </div>

          {/* Box 2: Company Personal Natal Risk */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <div className="text-xs uppercase font-medium text-slate-400 tracking-wider flex items-center justify-between">
              <span>{analysisData.symbol} Personal Micro Risk</span>
              <Cpu className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-3xl font-bold font-mono text-purple-400 my-3">
              {analysisData.company_micro_risk.toFixed(2)}
            </div>
            <p className="text-xs text-slate-400 leading-relaxed font-light">
              Incorporation chart Dasha & planetary transits (Sade Sati, Ketu/Sun).
            </p>
          </div>

          {/* Box 3: Dual Alignment Disaster Index */}
          <div className={`p-6 rounded-2xl border shadow-lg ${
            analysisData.dual_risk_index >= 7.0 
              ? 'bg-red-950/20 border-red-500/40' 
              : analysisData.dual_risk_index >= 5.0 
                ? 'bg-amber-950/20 border-amber-500/40' 
                : 'bg-emerald-950/20 border-emerald-500/40'
          }`}>
            <div className="text-xs uppercase font-medium tracking-wider flex items-center justify-between">
              <span className={analysisData.dual_risk_index >= 7.0 ? 'text-red-400' : 'text-slate-300'}>
                Dual Alignment Index
              </span>
              <AlertTriangle className={`w-4 h-4 ${analysisData.dual_risk_index >= 7.0 ? 'text-red-400 animate-pulse' : 'text-emerald-400'}`} />
            </div>
            <div className={`text-3xl font-bold font-mono my-3 ${
              analysisData.dual_risk_index >= 7.0 ? 'text-red-400' : analysisData.dual_risk_index >= 5.0 ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {analysisData.dual_risk_index.toFixed(2)} / 10
            </div>
            <div className={`text-xs font-semibold uppercase tracking-wider ${
              analysisData.dual_risk_index >= 7.0 ? 'text-red-400' : analysisData.dual_risk_index >= 5.0 ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {analysisData.recipe_status}
            </div>
          </div>
        </div>
      )}

      {/* Detail Breakdown & Signals */}
      {analysisData && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Disaster Recipe Explanation */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              Dual Alignment Risk Recipe Logic
            </h3>

            <div className="p-4 rounded-xl bg-[#080b11] border border-slate-800 text-xs leading-relaxed text-slate-300">
              {analysisData.recipe_desc}
            </div>

            <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between text-slate-400">
                <span>Asset / Company Name:</span>
                <span className="font-semibold text-slate-100">{analysisData.company_name}</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Category:</span>
                <span className="font-semibold text-amber-400 font-mono">{analysisData.category}</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Inception / Incorporation Date:</span>
                <span className="font-mono text-purple-400">{analysisData.incorporation_date}</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Market Sector:</span>
                <span className="font-semibold text-emerald-400">{analysisData.sector}</span>
              </div>
            </div>
          </div>

          {/* Right Column: Planetary Signals */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-400" />
              {analysisData.symbol} Natal Transit Telemetry Signals
            </h3>

            <div className="space-y-3">
              {analysisData.signals.map((sig, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-[#080b11] border border-slate-800 text-xs font-mono text-slate-300 flex items-start gap-3">
                  <ChevronRight className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <span>{sig}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
