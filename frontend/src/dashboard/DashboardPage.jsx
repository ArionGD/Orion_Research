import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Moon, 
  TrendingUp, 
  Layers, 
  RefreshCw, 
  LogOut, 
  User, 
  Building2,
  Filter,
  BarChart3,
  Calendar,
  Sparkles,
  AlertTriangle,
  Flame,
  Globe,
  Compass,
  MapPin,
  ShieldAlert
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import CompanyAnalysisPanel from '../company/CompanyAnalysisPanel';
import VedicResearchPanel from '../vedic/VedicResearchPanel';
import CommodityResearchPanel from '../commodities/CommodityResearchPanel';
import CustomDatePicker from '../components/CustomDatePicker';
import SectorSelectFilter from '../components/SectorSelectFilter';
import TelemetryConsolePanel from '../telemetry/TelemetryConsolePanel';
import MudraAIChatPanel from '../mudra/MudraAIChatPanel';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function DashboardPage({ onLogout }) {
  const [activeTab, setActiveTab] = useState('mudra');
  const [smiData, setSmiData] = useState(null);
  const [panchangaData, setPanchangaData] = useState(null);
  const [forecastData, setForecastData] = useState([]);
  const [selectedSector, setSelectedSector] = useState('All');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const healthRes = await fetch('/api/v1/health');
      if (healthRes.ok) setHealthStatus(await healthRes.json());

      const today = new Date().toISOString().split('T')[0];
      const smiRes = await fetch(`/smi/report?date=${today}`);
      if (smiRes.ok) setSmiData(await smiRes.json());

      const panRes = await fetch('/api/v1/vedic/panchanga');
      if (panRes.ok) setPanchangaData(await panRes.json());

      fetchForecast(startDate, selectedSector);
    } catch (err) {
      console.error('Error fetching telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchForecast = async (date, sector) => {
    try {
      const res = await fetch(`/smi/forecast?start_date=${date}&days=30&sector=${sector}`);
      if (res.ok) {
        const data = await res.json();
        setForecastData(data);
      }
    } catch (err) {
      console.error('Error fetching forecast:', err);
    }
  };

  const handleSectorChange = (sector) => {
    setSelectedSector(sector);
    fetchForecast(startDate, sector);
  };

  const formattedLabels = forecastData.map(d => {
    if (!d.date) return '';
    const parts = d.date.split('-');
    if (parts.length < 3) return d.date;
    return `${parseInt(parts[2], 10)}.${parseInt(parts[1], 10)}`;
  });

  const chartDataConfig = {
    labels: formattedLabels,
    datasets: [
      {
        label: `${selectedSector} Sector SMI Index`,
        data: forecastData.map(d => d.smi),
        borderColor: selectedSector === 'Energy' ? '#ef4444' : selectedSector === 'Technology' ? '#a855f7' : selectedSector === 'Banking' ? '#3b82f6' : '#f59e0b',
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          const color = selectedSector === 'Energy' ? 'rgba(239, 68, 68, 0.3)' : selectedSector === 'Technology' ? 'rgba(168, 85, 247, 0.3)' : 'rgba(245, 158, 11, 0.3)';
          gradient.addColorStop(0, color);
          gradient.addColorStop(1, 'rgba(14, 19, 31, 0.0)');
          return gradient;
        },
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: selectedSector === 'Energy' ? '#ef4444' : selectedSector === 'Technology' ? '#a855f7' : '#f59e0b',
        pointRadius: 4,
        pointHoverRadius: 7,
      }
    ]
  };

  const chartOptionsConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#0e131f',
        titleColor: '#f8fafc',
        bodyColor: '#f59e0b',
        borderColor: '#212b3e',
        borderWidth: 1,
        padding: 12,
        displayColors: false,
        callbacks: {
          title: (items) => {
            const idx = items[0].dataIndex;
            return forecastData[idx]?.date ? `Date: ${forecastData[idx].date}` : `Day: ${items[0].label}`;
          },
          label: (context) => ` SMI Risk Score: ${context.parsed.y} / 10.0`
        }
      }
    },
    scales: {
      x: {
        grid: { color: '#1e2638' },
        ticks: { 
          color: '#94a3b8', 
          font: { family: 'JetBrains Mono', size: 10 },
          maxRotation: 0,
          minRotation: 0
        }
      },
      y: {
        grid: { color: '#1e2638' },
        ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 } },
        min: 0,
        max: 10
      }
    }
  };

  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#080b11] text-slate-100 flex flex-col lg:flex-row relative overflow-x-hidden font-sans">
      {/* Mobile Top Header for Non-Mudra Tabs */}
      {activeTab !== 'mudra' && (
        <div className="lg:hidden h-14 px-4 bg-[#0e131f] border-b border-slate-800 flex items-center justify-between z-30 shrink-0 select-none">
          <button
            onClick={() => setMobileNavOpen(!mobileNavOpen)}
            className="flex items-center gap-2.5 group cursor-pointer"
            title="Toggle Navigation Menu"
          >
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-500 to-purple-600 flex items-center justify-center text-black font-bold text-sm shadow-md group-hover:scale-105 transition-transform">
              Ω
            </div>
            <div className="text-left">
              <span className="text-xs font-bold text-white tracking-tight block">ORION RESEARCH</span>
              <span className="text-[9px] font-mono text-amber-400 font-semibold block">Tap logo to menu</span>
            </div>
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setMobileNavOpen(!mobileNavOpen)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-700/80 text-amber-400 hover:text-white transition-all cursor-pointer"
            >
              <Activity className="w-4 h-4" />
            </button>
            <span className="px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[10px] font-mono font-bold">
              ACE v5.5
            </span>
          </div>
        </div>
      )}

      {/* Mobile Overlay Backdrop */}
      {mobileNavOpen && (
        <div
          onClick={() => setMobileNavOpen(false)}
          className="fixed inset-0 bg-black/75 backdrop-blur-sm z-40 lg:hidden transition-opacity"
        />
      )}

      {/* Left Navigation Sidebar (Collapsible Mobile Drawer + Desktop Static) */}
      <aside
        className={`fixed lg:relative inset-y-0 left-0 z-50 w-72 bg-[#0e131f] border-r border-slate-800/80 flex flex-col shrink-0 select-none transition-transform duration-300 ${
          mobileNavOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="p-5 sm:p-6 border-b border-slate-800/80 flex items-center justify-between">
          <button
            onClick={() => setMobileNavOpen(!mobileNavOpen)}
            className="flex items-center gap-3 text-left cursor-pointer group"
          >
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-amber-500 via-amber-600 to-purple-600 flex items-center justify-center text-black font-bold text-lg sm:text-xl shadow-lg shadow-amber-500/10 group-hover:scale-105 transition-transform">
              Ω
            </div>
            <div>
              <span className="text-sm sm:text-base font-bold tracking-tight text-white block">ORION RESEARCH</span>
              <span className="text-[10px] font-mono text-amber-500 font-semibold tracking-wider block">
                ACE v5.5 + VED ENGINE
              </span>
            </div>
          </button>
          <button
            onClick={() => setMobileNavOpen(false)}
            className="lg:hidden p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white"
          >
            ✕
          </button>
        </div>

        {/* Sidebar Nav Items */}
        <nav className="p-4 space-y-1 flex-1 overflow-y-auto">
          {[
            { id: 'mudra', label: '✦ Mudra AI Platform', icon: Sparkles },
            { id: 'executive', label: 'Executive Risk Dashboard', icon: Activity },
            { id: 'company', label: 'Company Chart & Dual Risk', icon: Building2 },
            { id: 'vedic', label: 'Ved Jyotish Research', icon: Moon },
            { id: 'commodities', label: 'Commodities & Energy', icon: TrendingUp },
            { id: 'telemetry', label: 'API Telemetry & Logs', icon: Layers },
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMobileNavOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all cursor-pointer ${
                  isActive 
                    ? 'bg-amber-500/10 text-white border-l-4 border-amber-500 font-semibold' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-amber-400' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Info & Logout */}
        <div className="p-4 border-t border-slate-800/80 space-y-3">
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-slate-900/60 border border-slate-800 text-xs">
            <User className="w-4 h-4 text-amber-400 shrink-0" />
            <div className="truncate">
              <span className="block text-slate-200 font-medium truncate">Superuser Admin</span>
              <span className="block text-[10px] text-slate-500 font-mono">ID: admin</span>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 text-xs font-semibold transition-all cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out Terminal</span>
          </button>
        </div>
      </aside>

      {/* Phone View Bottom Navigation Bar (5 Main Tabs) */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 z-40 h-20 bg-[#0e131f]/95 backdrop-blur-xl border-t border-slate-800 flex items-center justify-around px-3 shadow-2xl select-none">
        {[
          { id: 'mudra', label: 'Mudra AI', icon: Sparkles },
          { id: 'executive', label: 'Risk', icon: Activity },
          { id: 'company', label: 'Company', icon: Building2 },
          { id: 'vedic', label: 'Vedic', icon: Moon },
          { id: 'commodities', label: 'Commodity', icon: TrendingUp },
        ].map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => {
                setActiveTab(item.id);
                setMobileNavOpen(false);
              }}
              className={`flex flex-col items-center justify-center gap-1.5 py-2 px-3 rounded-2xl transition-all cursor-pointer ${
                isActive
                  ? 'text-amber-400 font-bold bg-amber-500/15 border border-amber-500/30 shadow-md shadow-amber-500/10'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-amber-400 scale-110' : 'text-slate-400'}`} />
              <span className="text-[11px] font-mono leading-none">{item.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main Content Workspace with Bottom Padding for Mobile Bottom Bar */}
      <main className={`flex-1 ${activeTab === 'mudra' ? 'h-[calc(100vh-5rem)] lg:h-screen overflow-hidden p-0 pb-20 lg:pb-0' : 'h-[calc(100vh-3.5rem)] lg:h-screen overflow-y-auto p-3 sm:p-6 lg:p-8 pb-24 lg:pb-8'}`}>
        {/* Render Mudra AI Full Screen */}
        {activeTab === 'mudra' && (
          <MudraAIChatPanel onToggleMobileNav={() => setMobileNavOpen(!mobileNavOpen)} />
        )}

        {/* Top Bar & Metrics (Hidden for Mudra AI Tab) */}
        {activeTab !== 'mudra' && (
          <>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 sm:mb-8">
              <div>
                <h1 className="text-lg sm:text-2xl font-extrabold text-white tracking-tight">
                  {activeTab === 'executive' && 'Executive Risk Dashboard'}
                  {activeTab === 'company' && 'Company Chart & Dual Alignment Risk'}
                  {activeTab === 'vedic' && 'Ved Jyotish Astronomical Research'}
                  {activeTab === 'commodities' && 'Commodity & Energy Intelligence'}
                  {activeTab === 'telemetry' && 'API Telemetry & Logs'}
                </h1>
                <p className="hidden sm:block text-slate-400 text-xs mt-1 font-light">
                  Mundane Astrological Analytics + Official VedAstro Jyotish Calculation Suite
                </p>
              </div>

              <div className="flex items-center gap-2 sm:gap-3">
                <button
                  onClick={fetchAllData}
                  className="px-3 py-1.5 sm:px-4 sm:py-2 rounded-xl bg-[#141a28] border border-slate-700/80 hover:border-slate-600 text-slate-200 text-xs font-medium flex items-center gap-2 transition-all cursor-pointer"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
                  <span>Refresh</span>
                </button>

                <span className="px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  READY
                </span>
              </div>
            </div>

            {/* Top Metric Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
                <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
                  Sovereign Malefic Index (SMI)
                </div>
                <div className="text-3xl font-bold font-mono text-amber-400 my-2">
                  {smiData?.smi ? smiData.smi.toFixed(2) : '5.42'}
                </div>
                <div className="text-xs text-slate-400">
                  Status: <span className="text-slate-200 font-medium">{smiData?.status || 'Active Operations'}</span>
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
                <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
                  System Risk Gravity
                </div>
                <div className="text-3xl font-bold font-mono text-blue-400 my-2">
                  {smiData?.system_gravity || 'NORMAL'}
                </div>
                <div className="text-xs text-slate-400">
                  Multi-planetary Alignment Severity
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
                <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
                  Ved Jyotish Engine Status
                </div>
                <div className="text-xl font-bold font-mono text-purple-400 my-3">
                  {healthStatus?.ved_engine_status || 'ONLINE'}
                </div>
                <div className="text-xs text-slate-400">
                  Official VedAstro 596+ Calculation Routines
                </div>
              </div>
            </div>
          </>
        )}

        {/* Tab 1: Executive Risk Dashboard */}
        {activeTab === 'executive' && (
          <div className="space-y-8">
            {/* Enhanced Chart Card with Premium Control Bar */}
            <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800/60">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
                    <BarChart3 className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white">
                      30-Day Forensic SMI Risk Forecast
                    </h3>
                    <p className="text-slate-400 text-xs font-light">
                      Showing sector-weighted malefic pressure trajectory
                    </p>
                  </div>
                </div>

                {/* Enhanced Controls Bar */}
                <div className="flex flex-wrap items-center gap-3">
                  {/* Custom Dark Sector Filter Component */}
                  <SectorSelectFilter
                    value={selectedSector}
                    onChange={handleSectorChange}
                  />

                  {/* Highlighted Custom Date Picker */}
                  <CustomDatePicker
                    value={startDate}
                    onChange={(newDate) => {
                      setStartDate(newDate);
                      fetchForecast(newDate, selectedSector);
                    }}
                    label="Start:"
                  />
                </div>
              </div>

              {/* Chart Canvas */}
              <div className="h-80">
                <Line data={chartDataConfig} options={chartOptionsConfig} />
              </div>
            </div>

            {/* Enhanced Telemetry Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Left Panel: Medini Active Yogas & Sector Volatility */}
              <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Flame className="w-4 h-4 text-amber-400" />
                    Medini Forensic Active Yogas & Sector Volatility
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400">
                    ASTRO CONFLICT ACTIVE
                  </span>
                </div>

                {/* Active Combination Highlight Card */}
                <div className="p-4 rounded-xl bg-[#141a28] border border-slate-800 space-y-2">
                  <div className="flex items-center gap-2 text-amber-400 font-bold text-xs font-mono">
                    <Sparkles className="w-4 h-4 shrink-0" />
                    <span>Graha Yudha (Mercury - Jupiter War)</span>
                  </div>
                  <p className="text-slate-300 text-xs leading-relaxed font-light">
                    Planetary War between Mercury (Intellect/Markets) and Jupiter (Capital/Expansion). Signals high market volatility and policy friction.
                  </p>
                </div>

                {/* Volatility Alert Badges */}
                <div className="space-y-2">
                  <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                    High Risk Sector Alerts:
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-mono flex items-center gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>Banking / Finance / Law</span>
                    </div>
                    <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-mono flex items-center gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>IT / Software / Telecom</span>
                    </div>
                    <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono flex items-center gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>Media & Publishing</span>
                    </div>
                    <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-mono flex items-center gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>Education & Policy</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Panel: Ved Jyotish Panchanga Structured Summary */}
              <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-purple-300 flex items-center gap-2">
                    <Moon className="w-4 h-4 text-purple-400" />
                    Ved Jyotish Daily Panchanga Summary
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/30 text-purple-300">
                    VEDASTRO ROUTINE
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-xl bg-[#141a28] border border-slate-800">
                    <span className="text-[10px] font-mono text-purple-400 block uppercase">1. Tithi (Phase)</span>
                    <span className="text-xs font-bold text-white font-mono block mt-1">
                      {panchangaData?.panchanga?.tithi || 'Shukla Navami'}
                    </span>
                  </div>

                  <div className="p-3 rounded-xl bg-[#141a28] border border-slate-800">
                    <span className="text-[10px] font-mono text-amber-400 block uppercase">2. Nakshatra</span>
                    <span className="text-xs font-bold text-white font-mono block mt-1">
                      {panchangaData?.panchanga?.nakshatra || 'Rohini'}
                    </span>
                  </div>

                  <div className="p-3 rounded-xl bg-[#141a28] border border-slate-800">
                    <span className="text-[10px] font-mono text-blue-400 block uppercase">3. Vara (Day)</span>
                    <span className="text-xs font-bold text-white font-mono block mt-1">
                      {panchangaData?.panchanga?.vara || 'Saturday'}
                    </span>
                  </div>

                  <div className="p-3 rounded-xl bg-[#141a28] border border-slate-800">
                    <span className="text-[10px] font-mono text-emerald-400 block uppercase">4. Yoga</span>
                    <span className="text-xs font-bold text-white font-mono block mt-1">
                      {panchangaData?.panchanga?.yoga || 'Shubha'}
                    </span>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-[#141a28] border border-slate-800 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between text-slate-400">
                    <span>Observation Coordinates:</span>
                    <span className="text-slate-200 font-mono">Mumbai (19.076° N, 72.877° E)</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-400">
                    <span>Ayanamsa System:</span>
                    <span className="text-amber-400 font-mono">Lahiri (Chitra Paksha)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Company Chart & Dual Risk */}
        {activeTab === 'company' && (
          <CompanyAnalysisPanel currentSmi={smiData?.smi || 5.5} />
        )}

        {/* Tab 3: Ved Jyotish Research */}
        {activeTab === 'vedic' && (
          <VedicResearchPanel />
        )}

        {/* Tab 4: Commodities & Energy */}
        {activeTab === 'commodities' && (
          <CommodityResearchPanel />
        )}

        {/* Tab 5: Telemetry Console */}
        {activeTab === 'telemetry' && (
          <TelemetryConsolePanel />
        )}
      </main>
    </div>
  );
}
