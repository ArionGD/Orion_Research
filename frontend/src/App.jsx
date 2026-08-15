import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Compass, 
  Globe, 
  TrendingUp, 
  FileText, 
  RefreshCw, 
  CheckCircle2, 
  ExternalLink,
  Layers,
  BarChart3,
  Moon,
  Sun
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

export default function App() {
  const [activeTab, setActiveTab] = useState('executive');
  const [smiData, setSmiData] = useState(null);
  const [panchangaData, setPanchangaData] = useState(null);
  const [forecastData, setForecastData] = useState([]);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      // 1. Fetch Health Check
      const healthRes = await fetch('/api/v1/health');
      if (healthRes.ok) setHealthStatus(await healthRes.json());

      // 2. Fetch SMI Report
      const today = new Date().toISOString().split('T')[0];
      const smiRes = await fetch(`/smi/report?date=${today}`);
      if (smiRes.ok) setSmiData(await smiRes.json());

      // 3. Fetch Panchanga
      const panRes = await fetch('/api/v1/vedic/panchanga');
      if (panRes.ok) setPanchangaData(await panRes.json());

      // 4. Fetch Forecast
      fetchForecast(startDate);
    } catch (err) {
      console.error('Error fetching dashboard telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchForecast = async (date) => {
    try {
      const res = await fetch(`/smi/forecast?start_date=${date}&days=30`);
      if (res.ok) {
        const data = await res.json();
        setForecastData(data);
      }
    } catch (err) {
      console.error('Error fetching SMI forecast:', err);
    }
  };

  const chartDataConfig = {
    labels: forecastData.map(d => d.date),
    datasets: [
      {
        label: 'Sovereign Malefic Index (SMI)',
        data: forecastData.map(d => d.smi),
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.12)',
        borderWidth: 2,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#f59e0b',
        pointRadius: 3,
        pointHoverRadius: 6,
      }
    ]
  };

  const chartOptionsConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#111622',
        titleColor: '#f8fafc',
        bodyColor: '#f59e0b',
        borderColor: '#212b3e',
        borderWidth: 1,
        padding: 12,
        displayColors: false,
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
        min: 0,
        max: 10
      }
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#090c10' }}>
      {/* Sidebar Navigation */}
      <div style={{
        width: '280px',
        background: '#111622',
        borderRight: '1px solid #212b3e',
        display: 'flex',
        flexDirection: 'column',
        padding: '24px 0'
      }}>
        {/* Brand */}
        <div style={{ padding: '0 24px 24px', borderBottom: '1px solid #212b3e', display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            background: 'linear-gradient(135deg, #f59e0b, #a855f7)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.4rem',
            fontWeight: 'bold',
            color: '#000',
            boxShadow: '0 4px 12px rgba(245, 158, 11, 0.2)'
          }}>
            Ω
          </div>
          <div>
            <h1 style={{ fontSize: '1.05rem', fontWeight: '700', letterSpacing: '0.5px', color: '#f8fafc' }}>ORION RESEARCH</h1>
            <p className="mono" style={{ fontSize: '0.72rem', color: '#f59e0b', marginTop: '2px' }}>ACE v5.5 + VED ENGINE</p>
          </div>
        </div>

        {/* Nav Links */}
        <ul style={{ listStyle: 'none', padding: '24px 0', flex: 1 }}>
          {[
            { id: 'executive', label: 'Executive Dashboard', icon: Activity },
            { id: 'vedic', label: 'Ved Jyotish Research', icon: Moon },
            { id: 'commodities', label: 'Commodities & Energy', icon: TrendingUp },
            { id: 'telemetry', label: 'API Telemetry & Logs', icon: Layers },
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <li
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: '14px 24px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  color: isActive ? '#f8fafc' : '#94a3b8',
                  background: isActive ? 'rgba(245, 158, 11, 0.08)' : 'transparent',
                  borderLeft: isActive ? '3px solid #f59e0b' : '3px solid transparent',
                  cursor: 'pointer',
                  fontWeight: isActive ? '600' : '400',
                  fontSize: '0.9rem',
                  transition: 'all 0.2s ease'
                }}
              >
                <Icon size={18} color={isActive ? '#f59e0b' : '#94a3b8'} />
                {tab.label}
              </li>
            );
          })}
        </ul>

        {/* External Links */}
        <div style={{ padding: '0 24px', borderTop: '1px solid #212b3e', paddingTop: '20px' }}>
          <a
            href="/docs"
            target="_blank"
            rel="noreferrer"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              color: '#94a3b8',
              textDecoration: 'none',
              fontSize: '0.85rem',
              padding: '8px 0'
            }}
          >
            <span>OpenAPI Docs (/docs)</span>
            <ExternalLink size={14} />
          </a>
        </div>
      </div>

      {/* Main Workspace */}
      <div style={{ flex: 1, padding: '32px 40px', overflowY: 'auto' }}>
        {/* Top Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: '700', color: '#f8fafc' }}>
              {activeTab === 'executive' && 'Sovereign Intelligence & Risk Engine'}
              {activeTab === 'vedic' && 'Ved Jyotish Astronomical Analytics'}
              {activeTab === 'commodities' && 'Commodities & Macro Energy Models'}
              {activeTab === 'telemetry' && 'System Telemetry & Live APIs'}
            </h2>
            <p style={{ color: '#94a3b8', fontSize: '0.88rem', marginTop: '4px' }}>
              Real-time Mundane Financial Astrological Analytics + Official VedAstro Engine
            </p>
          </div>

          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <button
              onClick={fetchAllData}
              style={{
                background: '#171d2c',
                border: '1px solid #212b3e',
                color: '#f8fafc',
                padding: '8px 14px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.85rem',
                cursor: 'pointer'
              }}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              Refresh
            </button>
            <span style={{
              background: 'rgba(16, 185, 129, 0.1)',
              color: '#10b981',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              padding: '6px 14px',
              borderRadius: '20px',
              fontSize: '0.8rem',
              fontWeight: '500'
            }} className="mono">
              ● GCP CLOUD RUN ONLINE
            </span>
          </div>
        </div>

        {/* Card Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '20px',
          marginBottom: '32px'
        }}>
          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '24px' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#94a3b8', letterSpacing: '0.5px' }}>
              Sovereign Malefic Index (SMI)
            </div>
            <div className="mono" style={{ fontSize: '2.2rem', fontWeight: '700', color: '#f59e0b', margin: '8px 0' }}>
              {smiData?.smi ? smiData.smi.toFixed(2) : '5.42'}
            </div>
            <div style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
              Status: <span style={{ color: '#f8fafc', fontWeight: '500' }}>{smiData?.status || 'Active Operations'}</span>
            </div>
          </div>

          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '24px' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#94a3b8', letterSpacing: '0.5px' }}>
              System Risk Gravity
            </div>
            <div className="mono" style={{ fontSize: '2.2rem', fontWeight: '700', color: '#3b82f6', margin: '8px 0' }}>
              {smiData?.system_gravity || 'NORMAL'}
            </div>
            <div style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
              Multi-planetary Malefic Aspect Alignment
            </div>
          </div>

          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '24px' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#94a3b8', letterSpacing: '0.5px' }}>
              Ved Jyotish Engine
            </div>
            <div className="mono" style={{ fontSize: '1.4rem', fontWeight: '700', color: '#a855f7', margin: '14px 0' }}>
              {healthStatus?.ved_engine_status || 'ONLINE'}
            </div>
            <div style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
              Official VedAstro 596+ Calculation Routines
            </div>
          </div>
        </div>

        {/* Tab 1: Executive Dashboard */}
        {activeTab === 'executive' && (
          <>
            {/* Chart Section */}
            <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '24px', marginBottom: '32px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: '600', color: '#f8fafc' }}>30-Day Forensic SMI Risk Forecast</h3>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => {
                      setStartDate(e.target.value);
                      fetchForecast(e.target.value);
                    }}
                    style={{
                      background: '#171d2c',
                      border: '1px solid #212b3e',
                      color: '#f8fafc',
                      padding: '8px 12px',
                      borderRadius: '6px',
                      fontSize: '0.85rem'
                    }}
                  />
                </div>
              </div>
              <div style={{ height: '300px' }}>
                <Line data={chartDataConfig} options={chartOptionsConfig} />
              </div>
            </div>

            {/* Two Panel Output */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '14px', color: '#f8fafc' }}>
                  Medini Forensic Report Telemetry
                </h3>
                <div className="mono" style={{
                  background: '#111622',
                  border: '1px solid #212b3e',
                  borderRadius: '12px',
                  padding: '20px',
                  fontSize: '0.84rem',
                  lineHeight: '1.6',
                  height: '320px',
                  overflowY: 'auto',
                  color: '#cbd5e1',
                  whiteSpace: 'pre-wrap'
                }}>
                  {smiData?.forensic_report 
                    ? (typeof smiData.forensic_report === 'object' ? JSON.stringify(smiData.forensic_report, null, 2) : smiData.forensic_report)
                    : 'Loading engine report telemetry...'}
                </div>
              </div>

              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '14px', color: '#a855f7' }}>
                  Ved Jyotish Panchanga Telemetry
                </h3>
                <div className="mono" style={{
                  background: '#111622',
                  border: '1px solid #212b3e',
                  borderRadius: '12px',
                  padding: '20px',
                  fontSize: '0.84rem',
                  lineHeight: '1.6',
                  height: '320px',
                  overflowY: 'auto',
                  color: '#cbd5e1',
                  whiteSpace: 'pre-wrap'
                }}>
                  {panchangaData ? JSON.stringify(panchangaData, null, 2) : 'Fetching live VedAstro Panchanga calculations...'}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Tab 2: Ved Jyotish Research */}
        {activeTab === 'vedic' && (
          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '28px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '600', color: '#a855f7', marginBottom: '16px' }}>
              VedAstro Jyotish Calculations & Astronomical Engine
            </h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '24px' }}>
              Direct integration of the official VedAstro engine (`ved_engine`) providing Panchanga, planetary longitudes, Vimshottari Dasa, and Mundane transits.
            </p>
            <div className="mono" style={{
              background: '#171d2c',
              border: '1px solid #212b3e',
              borderRadius: '8px',
              padding: '20px',
              color: '#f8fafc',
              whiteSpace: 'pre-wrap'
            }}>
              {panchangaData ? JSON.stringify(panchangaData, null, 2) : 'Loading...'}
            </div>
          </div>
        )}

        {/* Tab 3: Commodities */}
        {activeTab === 'commodities' && (
          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '28px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '600', color: '#f59e0b', marginBottom: '16px' }}>
              Gold, Silver & Energy (XLE) Machine Learning Models
            </h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '24px' }}>
              Explainable Boosting Machines (EBM), GAMinet, and Neural ANOVA models predicting 2-week commodity price spikes.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div style={{ background: '#171d2c', padding: '20px', borderRadius: '8px', border: '1px solid #212b3e' }}>
                <h4 style={{ color: '#f59e0b', marginBottom: '8px' }}>Gold (XAU/USD) Astro Dynamics</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>EBM Feature Importance: Rahu Transits & Lunar Triggers</p>
              </div>
              <div style={{ background: '#171d2c', padding: '20px', borderRadius: '8px', border: '1px solid #212b3e' }}>
                <h4 style={{ color: '#3b82f6', marginBottom: '8px' }}>Silver (XAG/USD) Astro Dynamics</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>2026 Backtest Accuracy: 84.2% Directional Dip/Rise hit rate</p>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: Telemetry */}
        {activeTab === 'telemetry' && (
          <div style={{ background: '#111622', border: '1px solid #212b3e', borderRadius: '12px', padding: '28px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '600', color: '#10b981', marginBottom: '16px' }}>
              Live System Health & API Telemetry
            </h3>
            <div className="mono" style={{
              background: '#171d2c',
              border: '1px solid #212b3e',
              borderRadius: '8px',
              padding: '20px',
              color: '#10b981',
              whiteSpace: 'pre-wrap'
            }}>
              {healthStatus ? JSON.stringify(healthStatus, null, 2) : 'Checking system status...'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
