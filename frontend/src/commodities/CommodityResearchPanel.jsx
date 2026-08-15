import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Coins, 
  Flame, 
  Sparkles, 
  Activity, 
  ShieldCheck, 
  AlertCircle,
  BarChart3,
  Calendar,
  Layers
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

export default function CommodityResearchPanel() {
  const [activeAsset, setActiveAsset] = useState('gold');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCommodityData(activeAsset);
  }, [activeAsset]);

  const fetchCommodityData = async (asset) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/commodities/forecast?commodity=${asset}`);
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (err) {
      console.error('Error fetching commodity forecast:', err);
    } finally {
      setLoading(false);
    }
  };

  const chartDataConfig = {
    labels: data?.forecast ? data.forecast.map(d => d.date) : [],
    datasets: [
      {
        label: 'Up Probability',
        data: data?.forecast ? data.forecast.map(d => (d.probability * 100).toFixed(1)) : [],
        borderColor: activeAsset === 'gold' ? '#f59e0b' : activeAsset === 'silver' ? '#3b82f6' : '#ef4444',
        backgroundColor: activeAsset === 'gold' ? 'rgba(245, 158, 11, 0.15)' : activeAsset === 'silver' ? 'rgba(59, 130, 246, 0.15)' : 'rgba(239, 68, 68, 0.15)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: activeAsset === 'gold' ? '#f59e0b' : activeAsset === 'silver' ? '#3b82f6' : '#ef4444',
        pointRadius: 4,
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
        callbacks: {
          label: (context) => ` Up Probability: ${context.parsed.y}%`
        }
      }
    },
    scales: {
      x: {
        grid: { color: '#1e2638' },
        ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 } }
      },
      y: {
        grid: { color: '#1e2638' },
        ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 } },
        min: 30,
        max: 80
      }
    }
  };

  return (
    <div className="space-y-6 sm:space-y-8">
      {/* Top Asset Selector Banner */}
      <div className="p-4 sm:p-8 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-xl relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-amber-500/10 blur-[100px] rounded-full pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono mb-3">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Predictive Commodity Astrological Models</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white tracking-tight">
              Gold, Silver & Energy (Crude Oil / Gas) Analytics
            </h2>
            <p className="text-slate-400 text-xs mt-1 font-light max-w-2xl">
              Explainable Boosting Machines (EBM), Neural ANOVA, and Conflict Supply Shock Models predicting 2-week price movements.
            </p>
          </div>

          {/* Commodity Asset Selector Tabs */}
          <div className="flex flex-wrap gap-2">
            {[
              { id: 'gold', label: '🪙 Gold (XAU)', color: 'amber' },
              { id: 'silver', label: '🥈 Silver (XAG)', color: 'blue' },
              { id: 'oil', label: '🛢️ Crude Oil & Gas (XLE)', color: 'red' },
            ].map(asset => (
              <button
                key={asset.id}
                onClick={() => setActiveAsset(asset.id)}
                className={`px-4 py-2.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                  activeAsset === asset.id
                    ? 'bg-gradient-to-r from-amber-500 to-amber-600 text-black shadow-lg shadow-amber-500/20'
                    : 'bg-[#141a28] border border-slate-700/80 text-slate-300 hover:border-slate-500'
                }`}
              >
                {asset.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Metric Header Cards */}
      {data && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
              Asset Designation
            </div>
            <div className="text-xl font-bold text-white my-2 font-mono">
              {data.asset}
            </div>
            <div className="text-xs text-amber-400 font-mono">
              {data.accuracy}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
              Ruling Astrological Factor
            </div>
            <div className="text-sm font-bold text-purple-400 my-2">
              {data.ruling_astrology}
            </div>
            <div className="text-xs text-slate-400">
              Mundane Planetary Transit Driver
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <div className="text-xs uppercase font-medium text-slate-400 tracking-wider">
              Model Framework
            </div>
            <div className="text-sm font-bold text-emerald-400 my-2 font-mono">
              EBM + GAMinet Neural ANOVA
            </div>
            <div className="text-xs text-slate-400">
              Feature Importance & Causal Wavelets
            </div>
          </div>
        </div>
      )}

      {/* Chart & Detailed Table */}
      {data?.forecast && (
        <div className="space-y-8">
          {/* Probability Trend Chart */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg">
            <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-amber-400" />
              2-Week Price Direction Up-Probability Curve (%)
            </h3>
            <div className="h-72">
              <Line data={chartDataConfig} options={chartOptionsConfig} />
            </div>
          </div>

          {/* Detailed Predictions Table */}
          <div className="p-6 rounded-2xl bg-[#0e131f] border border-slate-800/90 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Calendar className="w-4 h-4 text-amber-400" />
              Daily Forecast Telemetry & Sniper Alert Signals
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono uppercase text-slate-400">
                    <th className="py-3 px-4">Date</th>
                    <th className="py-3 px-4">Predicted Direction</th>
                    <th className="py-3 px-4">Up Probability</th>
                    <th className="py-3 px-4">Sniper Alert Probability</th>
                    <th className="py-3 px-4">SMI Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
                  {data.forecast.map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-3 px-4 text-slate-300">{row.date}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2.5 py-1 rounded-md text-[11px] font-bold ${
                          row.direction === 'UP' 
                            ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400' 
                            : 'bg-red-500/10 border border-red-500/30 text-red-400'
                        }`}>
                          {row.direction === 'UP' ? '▲ UP' : '▼ DOWN'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-amber-400 font-bold">
                        {(row.probability * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-4 text-slate-300">
                        {row.sniper_alert ? (row.sniper_alert * 100).toFixed(2) + '%' : row.alert || 'Nominal'}
                      </td>
                      <td className="py-3 px-4 text-purple-400">
                        {row.smi || row.oil_smi || '5.5'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
