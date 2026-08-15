import React, { useState, useRef, useEffect } from 'react';
import { Filter, ChevronDown, Check, Sparkles } from 'lucide-react';

const SECTORS = [
  { id: 'All', label: 'All Sectors Baseline', ruling: 'General Macro Baseline', color: 'text-amber-400', badgeBg: 'bg-amber-500/10 border-amber-500/30' },
  { id: 'Technology', label: 'Technology', ruling: 'Mercury / Rahu', color: 'text-purple-400', badgeBg: 'bg-purple-500/10 border-purple-500/30' },
  { id: 'Banking', label: 'Banking & Finance', ruling: 'Jupiter / Moon', color: 'text-blue-400', badgeBg: 'bg-blue-500/10 border-blue-500/30' },
  { id: 'Energy', label: 'Energy & Oil', ruling: 'Mars / Saturn', color: 'text-red-400', badgeBg: 'bg-red-500/10 border-red-500/30' },
  { id: 'Defense', label: 'Defense & Aerospace', ruling: 'Mars / Ketu', color: 'text-orange-400', badgeBg: 'bg-orange-500/10 border-orange-500/30' },
  { id: 'Metals', label: 'Precious Metals', ruling: 'Gold / Silver / Sun', color: 'text-emerald-400', badgeBg: 'bg-emerald-500/10 border-emerald-500/30' }
];

export default function SectorSelectFilter({ value = 'All', onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const selectedSector = SECTORS.find(s => s.id === value) || SECTORS[0];

  // Click outside to close
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleSelect = (sectorId) => {
    onChange(sectorId);
    setIsOpen(false);
  };

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2.5 bg-[#171e2e] hover:bg-[#1f283d] border border-slate-700/80 hover:border-slate-500 px-3.5 py-2 rounded-xl text-xs font-mono font-semibold transition-all cursor-pointer shadow-lg active:scale-95"
      >
        <Filter className="w-3.5 h-3.5 text-amber-400 shrink-0" />
        <span className="text-slate-400">Sector:</span>
        <span className={`font-bold ${selectedSector.color}`}>
          {selectedSector.label}
        </span>
        <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Custom Dark Popover Menu */}
      {isOpen && (
        <div className="absolute left-0 mt-2 w-72 bg-[#0e131f] border border-slate-700/90 rounded-2xl p-2 shadow-2xl z-50 animate-in fade-in zoom-in-95 duration-150 space-y-1">
          <div className="px-3 py-2 text-[10px] font-mono uppercase text-slate-400 border-b border-slate-800 flex items-center justify-between">
            <span>Select Astrological Sector</span>
            <Sparkles className="w-3 h-3 text-amber-400" />
          </div>

          <div className="space-y-1 pt-1">
            {SECTORS.map((sector) => {
              const isSelected = sector.id === value;
              return (
                <button
                  key={sector.id}
                  type="button"
                  onClick={() => handleSelect(sector.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-mono transition-all cursor-pointer ${
                    isSelected
                      ? `${sector.badgeBg} border text-white font-bold`
                      : 'hover:bg-[#171e2e] text-slate-300'
                  }`}
                >
                  <div className="flex flex-col text-left">
                    <span className={`font-bold ${sector.color}`}>{sector.label}</span>
                    <span className="text-[10px] text-slate-500 font-light">{sector.ruling}</span>
                  </div>

                  {isSelected && (
                    <Check className={`w-4 h-4 ${sector.color} shrink-0`} />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
