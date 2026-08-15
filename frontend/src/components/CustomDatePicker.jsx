import React, { useState, useRef, useEffect } from 'react';
import { Calendar, ChevronLeft, ChevronRight, Sparkles, Check } from 'lucide-react';

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

const DAY_NAMES = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

export default function CustomDatePicker({ value, onChange, label = "Start:" }) {
  const [isOpen, setIsOpen] = useState(false);
  const popoverRef = useRef(null);

  // Parse input value (YYYY-MM-DD)
  const parseDate = (valStr) => {
    try {
      const parts = valStr.split('-');
      if (parts.length === 3) {
        return new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
      }
    } catch (e) {}
    return new Date();
  };

  const selectedDate = parseDate(value);
  const [currentViewDate, setCurrentViewDate] = useState(selectedDate);

  useEffect(() => {
    setCurrentViewDate(parseDate(value));
  }, [value]);

  // Close popover when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target)) {
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

  const viewYear = currentViewDate.getFullYear();
  const viewMonth = currentViewDate.getMonth();

  const handlePrevMonth = () => {
    setCurrentViewDate(new Date(viewYear, viewMonth - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentViewDate(new Date(viewYear, viewMonth + 1, 1));
  };

  const handleSelectDay = (day) => {
    const newDate = new Date(viewYear, viewMonth, day);
    const yyyy = newDate.getFullYear();
    const mm = String(newDate.getMonth() + 1).padStart(2, '0');
    const dd = String(newDate.getDate()).padStart(2, '0');
    const iso = `${yyyy}-${mm}-${dd}`;
    onChange(iso);
    setIsOpen(false);
  };

  const handleSetToday = () => {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const iso = `${yyyy}-${mm}-${dd}`;
    onChange(iso);
    setCurrentViewDate(today);
    setIsOpen(false);
  };

  // Generate calendar matrix for month
  const firstDayOfMonth = new Date(viewYear, viewMonth, 1).getDay();
  const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();

  // Days array
  const daysGrid = [];
  for (let i = 0; i < firstDayOfMonth; i++) {
    daysGrid.push(null);
  }
  for (let d = 1; d <= daysInMonth; d++) {
    daysGrid.push(d);
  }

  // Format display text on trigger button
  const displayFormattedDate = `${String(selectedDate.getDate()).padStart(2, '0')}-${String(selectedDate.getMonth() + 1).padStart(2, '0')}-${selectedDate.getFullYear()}`;

  return (
    <div className="relative inline-block text-left" ref={popoverRef}>
      {/* Highlighted Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 bg-[#171e2e] hover:bg-[#1f283d] border border-amber-500/40 hover:border-amber-400 px-3.5 py-2 rounded-xl text-xs font-mono font-semibold transition-all cursor-pointer shadow-lg shadow-amber-500/5 active:scale-95"
      >
        <Calendar className="w-4 h-4 text-amber-400 shrink-0" />
        <span className="text-slate-400">{label}</span>
        <span className="text-amber-300 font-bold tracking-wider">{displayFormattedDate}</span>
      </button>

      {/* Custom Dark Theme Popover */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-72 bg-[#0e131f] border border-slate-700/90 rounded-2xl p-4 shadow-2xl z-[100] animate-in fade-in zoom-in-95 duration-150">
          {/* Calendar Header: Month + Year + Nav */}
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
            <span className="text-sm font-bold text-white font-mono flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              {MONTH_NAMES[viewMonth]} {viewYear}
            </span>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handlePrevMonth}
                className="p-1.5 rounded-lg bg-[#171e2e] hover:bg-[#222b3e] text-slate-300 transition-colors cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={handleNextMonth}
                className="p-1.5 rounded-lg bg-[#171e2e] hover:bg-[#222b3e] text-slate-300 transition-colors cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Weekday Labels */}
          <div className="grid grid-cols-7 gap-1 text-center mb-2">
            {DAY_NAMES.map(name => (
              <span key={name} className="text-[11px] font-mono font-bold text-slate-500">
                {name}
              </span>
            ))}
          </div>

          {/* Days Grid */}
          <div className="grid grid-cols-7 gap-1 text-center">
            {daysGrid.map((day, idx) => {
              if (day === null) {
                return <div key={`empty-${idx}`} className="h-8" />;
              }

              const isSelected = 
                day === selectedDate.getDate() &&
                viewMonth === selectedDate.getMonth() &&
                viewYear === selectedDate.getFullYear();

              const isToday = 
                day === new Date().getDate() &&
                viewMonth === new Date().getMonth() &&
                viewYear === new Date().getFullYear();

              return (
                <button
                  key={day}
                  type="button"
                  onClick={() => handleSelectDay(day)}
                  className={`h-8 rounded-lg text-xs font-mono font-medium transition-all cursor-pointer flex items-center justify-center ${
                    isSelected
                      ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/30'
                      : isToday
                        ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                        : 'text-slate-300 hover:bg-[#1b2334] hover:text-white'
                  }`}
                >
                  {day}
                </button>
              );
            })}
          </div>

          {/* Quick Footer Controls */}
          <div className="flex items-center justify-between pt-3 mt-3 border-t border-slate-800 text-[11px] font-mono">
            <button
              type="button"
              onClick={handleSetToday}
              className="text-amber-400 hover:text-amber-300 font-semibold cursor-pointer"
            >
              Today
            </button>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="text-slate-500 hover:text-slate-300 cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
