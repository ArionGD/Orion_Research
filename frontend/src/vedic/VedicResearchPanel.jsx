import React, { useState, useEffect } from 'react';
import { 
  Moon, 
  Sun, 
  Sparkles, 
  MapPin, 
  Calendar, 
  Compass, 
  Globe, 
  RefreshCw, 
  Layers, 
  ShieldCheck,
  Zap,
  Info
} from 'lucide-react';
import CustomDatePicker from '../components/CustomDatePicker';

export default function VedicResearchPanel() {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [city, setCity] = useState('Mumbai');
  const [panchanga, setPanchanga] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPanchanga(selectedDate);
  }, [selectedDate]);

  const fetchPanchanga = async (date) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/vedic/panchanga?date=${date}`);
      if (res.ok) {
        const data = await res.json();
        setPanchanga(data);
      }
    } catch (err) {
      console.error('Error fetching Panchanga:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 sm:space-y-8">
      {/* Top Banner */}
      <div className="p-4 sm:p-8 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-xl relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600/10 blur-[100px] rounded-full pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-mono mb-3">
              <Moon className="w-3.5 h-3.5" />
              <span>Official VedAstro Jyotish Engine</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white tracking-tight">
              Panchanga & Planetary Transit Research Suite
            </h2>
            <p className="text-slate-400 text-xs mt-1 font-light max-w-2xl">
              High-precision astronomical calculations powered by `ved_engine` delivering real-time Tithi, Nakshatra, Yoga, Karana, Ayanamsa, and planetary longitudes.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <CustomDatePicker
              value={selectedDate}
              onChange={(newDate) => setSelectedDate(newDate)}
              label="Date:"
            />

            <button
              onClick={() => fetchPanchanga(selectedDate)}
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center gap-2 transition-all cursor-pointer shadow-lg shadow-purple-600/20"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Compute Panchanga</span>
            </button>
          </div>
        </div>
      </div>

      {/* 5 Panchanga Core Elements Grid */}
      {panchanga?.panchanga && (
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            The 5 Core Elements of Panchanga (Five Limbs of Time)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
            {/* Tithi */}
            <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg relative overflow-hidden group hover:border-purple-500/40 transition-all">
              <div className="text-[10px] uppercase font-mono font-semibold text-purple-400 tracking-wider mb-2 flex items-center justify-between">
                <span>1. Tithi (Lunar Phase)</span>
                <Moon className="w-3.5 h-3.5 text-purple-400" />
              </div>
              <div className="text-lg font-bold text-white mb-1 font-mono">
                {panchanga.panchanga.tithi}
              </div>
              <div className="text-[11px] text-slate-400 font-light">
                Distance between Sun & Moon
              </div>
            </div>

            {/* Nakshatra */}
            <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg relative overflow-hidden group hover:border-amber-500/40 transition-all">
              <div className="text-[10px] uppercase font-mono font-semibold text-amber-400 tracking-wider mb-2 flex items-center justify-between">
                <span>2. Nakshatra (Star)</span>
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              </div>
              <div className="text-lg font-bold text-white mb-1 font-mono">
                {panchanga.panchanga.nakshatra}
              </div>
              <div className="text-[11px] text-slate-400 font-light">
                Lunar Mansion position
              </div>
            </div>

            {/* Vara */}
            <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg relative overflow-hidden group hover:border-blue-500/40 transition-all">
              <div className="text-[10px] uppercase font-mono font-semibold text-blue-400 tracking-wider mb-2 flex items-center justify-between">
                <span>3. Vara (Solar Day)</span>
                <Sun className="w-3.5 h-3.5 text-blue-400" />
              </div>
              <div className="text-lg font-bold text-white mb-1 font-mono">
                {panchanga.panchanga.vara}
              </div>
              <div className="text-[11px] text-slate-400 font-light">
                Ruling Solar Day Lord
              </div>
            </div>

            {/* Yoga */}
            <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg relative overflow-hidden group hover:border-emerald-500/40 transition-all">
              <div className="text-[10px] uppercase font-mono font-semibold text-emerald-400 tracking-wider mb-2 flex items-center justify-between">
                <span>4. Yoga (Solilunar)</span>
                <Zap className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <div className="text-lg font-bold text-white mb-1 font-mono">
                {panchanga.panchanga.yoga}
              </div>
              <div className="text-[11px] text-slate-400 font-light">
                Sum of Sun & Moon longitudes
              </div>
            </div>

            {/* Karana */}
            <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg relative overflow-hidden group hover:border-rose-500/40 transition-all">
              <div className="text-[10px] uppercase font-mono font-semibold text-rose-400 tracking-wider mb-2 flex items-center justify-between">
                <span>5. Karana (Half Tithi)</span>
                <Compass className="w-3.5 h-3.5 text-rose-400" />
              </div>
              <div className="text-lg font-bold text-white mb-1 font-mono">
                {panchanga.panchanga.karana}
              </div>
              <div className="text-[11px] text-slate-400 font-light">
                Action & execution quality
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Planetary Transit Breakdown Matrix */}
      {panchanga?.astronomical_weather && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Planetary Transits */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Globe className="w-4 h-4 text-purple-400" />
              Mundane Planetary Transit Alignment
            </h3>

            <div className="space-y-3">
              <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-amber-400 block">Jupiter (Guru) Transit</span>
                  <span className="text-slate-400 text-xs font-light">Expansion, banking & systemic capital</span>
                </div>
                <span className="px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 font-mono text-xs font-semibold">
                  {panchanga.astronomical_weather.jupiter_transit}
                </span>
              </div>

              <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-blue-400 block">Saturn (Shani) Transit</span>
                  <span className="text-slate-400 text-xs font-light">Structure, commodities & labor friction</span>
                </div>
                <span className="px-3 py-1 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-300 font-mono text-xs font-semibold">
                  {panchanga.astronomical_weather.saturn_transit}
                </span>
              </div>

              <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-purple-400 block">Rahu-Ketu Nodal Axis</span>
                  <span className="text-slate-400 text-xs font-light">Tech disruptions, AI adoption & market spikes</span>
                </div>
                <span className="px-3 py-1 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono text-xs font-semibold">
                  {panchanga.astronomical_weather.rahu_ketu_axis}
                </span>
              </div>
            </div>
          </div>

          {/* Right Column: Ephemeris Metadata & Ayanamsa */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <MapPin className="w-4 h-4 text-emerald-400" />
              Ephemeris & Coordinates Configuration
            </h3>

            <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 space-y-3 text-xs">
              <div className="flex items-center justify-between text-slate-400">
                <span>Calculation Engine:</span>
                <span className="font-semibold text-purple-400 font-mono">VedAstro REST Engine</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Ayanamsa System:</span>
                <span className="font-semibold text-amber-400 font-mono">
                  {panchanga.panchanga?.ayanamsa || 'Lahiri (Chitra Paksha)'}
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Observation Location:</span>
                <span className="font-semibold text-slate-200">
                  {panchanga.location?.city} ({panchanga.location?.latitude}° N, {panchanga.location?.longitude}° E)
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>House System:</span>
                <span className="font-semibold text-emerald-400 font-mono">Equal House / Sripati</span>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-purple-500/5 border border-purple-500/20 text-purple-300 text-xs leading-relaxed flex items-start gap-2">
              <Info className="w-4 h-4 shrink-0 text-purple-400 mt-0.5" />
              <span>
                VedAstro engine calculations provide accurate planetary longitudes used to evaluate both Mundane Market SMI Weather and Company Horoscopes.
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
