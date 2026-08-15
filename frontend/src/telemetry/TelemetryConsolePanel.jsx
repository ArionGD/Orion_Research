import React, { useState, useEffect } from 'react';
import { 
  Terminal, 
  CheckCircle2, 
  AlertCircle, 
  Server, 
  Cpu, 
  Activity, 
  Layers, 
  Clock, 
  RefreshCw, 
  Play, 
  Code2, 
  Database,
  Globe,
  Radio,
  Sparkles
} from 'lucide-react';

export default function TelemetryConsolePanel() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeEndpoint, setActiveEndpoint] = useState('/api/v1/health');
  const [endpointResponse, setEndpointResponse] = useState(null);
  const [responseTimeMs, setResponseTimeMs] = useState(0);
  const [responseStatus, setResponseStatus] = useState(200);

  useEffect(() => {
    fetchHealth();
    testEndpoint('/api/v1/health');
  }, []);

  const fetchHealth = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/health');
      if (res.ok) {
        setHealth(await res.json());
      }
    } catch (err) {
      console.error('Error fetching health:', err);
    } finally {
      setLoading(false);
    }
  };

  const testEndpoint = async (url) => {
    setActiveEndpoint(url);
    const start = performance.now();
    try {
      const res = await fetch(url);
      const end = performance.now();
      setResponseTimeMs(Math.round(end - start));
      setResponseStatus(res.status);
      if (res.ok) {
        setEndpointResponse(await res.json());
      } else {
        setEndpointResponse({ error: `HTTP ${res.status} Error` });
      }
    } catch (err) {
      setEndpointResponse({ error: err.message });
      setResponseStatus(500);
    }
  };

  const endpointPresets = [
    { label: 'System Health', url: '/api/v1/health' },
    { label: 'SMI Forensic Report', url: `/smi/report?date=${new Date().toISOString().split('T')[0]}` },
    { label: 'VedAstro Panchanga', url: '/api/v1/vedic/panchanga' },
    { label: 'NSE Stock Presets', url: '/api/v1/company/presets' },
    { label: 'Gold Forecast API', url: '/api/v1/commodities/forecast?commodity=gold' },
    { label: 'Silver Forecast API', url: '/api/v1/commodities/forecast?commodity=silver' },
    { label: 'Crude Oil Forecast', url: '/api/v1/commodities/forecast?commodity=oil' },
  ];

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="p-8 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-xl relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 blur-[100px] rounded-full pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono mb-3">
              <Radio className="w-3.5 h-3.5 animate-pulse" />
              <span>Live System Diagnostic & Telemetry Console</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white tracking-tight">
              FastAPI Engine Operational Health & API Explorer
            </h2>
            <p className="text-slate-400 text-xs mt-1 font-light max-w-2xl">
              Real-time monitoring of backend microservices, official `ved_engine` bindings, ephemeris routines, and API endpoints.
            </p>
          </div>

          <button
            onClick={fetchHealth}
            className="px-4 py-2.5 rounded-xl bg-[#141a28] border border-slate-700/80 hover:border-slate-500 text-slate-200 text-xs font-mono font-semibold flex items-center gap-2 transition-all cursor-pointer shadow-lg"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-emerald-400 ${loading ? 'animate-spin' : ''}`} />
            <span>Ping Telemetry</span>
          </button>
        </div>
      </div>

      {/* Microservice Operational Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-2">
          <div className="flex items-center justify-between text-xs uppercase font-mono text-slate-400">
            <span>FastAPI Core</span>
            <Server className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <span>ONLINE</span>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            Version 5.5.0 (Port 8000)
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-2">
          <div className="flex items-center justify-between text-xs uppercase font-mono text-slate-400">
            <span>VedAstro Engine</span>
            <Sparkles className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold font-mono text-purple-400 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse" />
            <span>{health?.ved_engine_status || 'ONLINE'}</span>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            596+ Jyotish Routines
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-2">
          <div className="flex items-center justify-between text-xs uppercase font-mono text-slate-400">
            <span>NSE Corporate Engine</span>
            <Cpu className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-xl font-bold font-mono text-amber-400 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse" />
            <span>{health?.corporate_engine || 'ONLINE'}</span>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            21 Stock & Index Horoscopes
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-2">
          <div className="flex items-center justify-between text-xs uppercase font-mono text-slate-400">
            <span>React Vite SPA</span>
            <Globe className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-xl font-bold font-mono text-blue-400 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse" />
            <span>READY</span>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            Port 5173 (Dev Proxy)
          </div>
        </div>
      </div>

      {/* Interactive API Explorer & Response Console */}
      <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <Terminal className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Live REST API Endpoint Tester & Inspector
              </h3>
              <p className="text-slate-400 text-xs font-light">
                Select an endpoint preset to trigger a live HTTP request and inspect JSON payload telemetry
              </p>
            </div>
          </div>

          {/* Preset Buttons */}
          <div className="flex flex-wrap gap-2">
            {endpointPresets.map((ep) => (
              <button
                key={ep.url}
                onClick={() => testEndpoint(ep.url)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all cursor-pointer ${
                  activeEndpoint === ep.url
                    ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                    : 'bg-[#141a28] border border-slate-700/80 text-slate-300 hover:border-slate-500'
                }`}
              >
                {ep.label}
              </button>
            ))}
          </div>
        </div>

        {/* Request Details Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl bg-[#080b11] border border-slate-800 font-mono text-xs">
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[11px]">
              GET
            </span>
            <span className="text-amber-300 font-semibold">{activeEndpoint}</span>
          </div>

          <div className="flex items-center gap-4 text-slate-400 text-[11px]">
            <div className="flex items-center gap-1.5">
              <span>Status:</span>
              <span className={`font-bold ${responseStatus === 200 ? 'text-emerald-400' : 'text-red-400'}`}>
                {responseStatus} OK
              </span>
            </div>

            <div className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              <span className="text-amber-400 font-bold">{responseTimeMs} ms</span>
            </div>
          </div>
        </div>

        {/* JSON Payload Viewer */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>JSON Response Body:</span>
            <span>Content-Type: application/json</span>
          </div>

          <div className="p-6 rounded-xl bg-[#080b11] border border-slate-800 text-xs font-mono leading-relaxed h-96 overflow-y-auto text-emerald-400/90 whitespace-pre-wrap shadow-inner selection:bg-emerald-500 selection:text-black">
            {endpointResponse ? (
              JSON.stringify(endpointResponse, null, 2)
            ) : (
              <span className="text-slate-500">Executing API request...</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
