import React, { useState } from 'react';
import { Lock, User, KeyRound, AlertCircle, ArrowLeft, ShieldCheck } from 'lucide-react';

export default function LoginPage({ onLoginSuccess, onBackToLanding }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const adminUser = import.meta.env.VITE_ADMIN_USER || 'admin';
  const adminPass = import.meta.env.VITE_ADMIN_PASS || 'password';

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    setTimeout(() => {
      if (username.trim() === adminUser && password === adminPass) {
        localStorage.setItem('orion_auth_user', username);
        onLoginSuccess();
      } else {
        setError('Invalid Superuser Credentials. Default ID: admin, Password: password');
        setIsSubmitting(false);
      }
    }, 400);
  };

  return (
    <div className="min-h-screen bg-[#080b11] text-slate-100 flex items-center justify-center p-6 relative overflow-hidden font-sans">
      {/* Glow effect */}
      <div className="absolute w-[500px] h-[300px] bg-gradient-to-tr from-amber-500/10 via-purple-600/10 to-blue-600/10 blur-[130px] rounded-full pointer-events-none" />

      {/* Back button */}
      <button
        onClick={onBackToLanding}
        className="absolute top-8 left-8 flex items-center gap-2 text-slate-400 hover:text-white text-sm font-medium transition-colors cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Landing Page</span>
      </button>

      <div className="w-full max-w-md bg-[#0e131f] border border-slate-800/90 rounded-2xl p-8 shadow-2xl relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-500 via-amber-600 to-purple-600 flex items-center justify-center text-black font-bold text-2xl mx-auto mb-4 shadow-lg shadow-amber-500/20">
            Ω
          </div>
          <h2 className="text-2xl font-extrabold text-white tracking-tight">Superuser Admin Portal</h2>
          <p className="text-slate-400 text-xs mt-1 font-mono">
            ORION SOVEREIGN RESEARCH & VED ENGINE
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-start gap-3">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Superuser ID
            </label>
            <div className="relative">
              <User className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                className="w-full bg-[#141a28] border border-slate-700/80 focus:border-amber-500 text-slate-100 pl-11 pr-4 py-3 rounded-xl text-sm outline-none transition-colors font-mono"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Admin Password
            </label>
            <div className="relative">
              <KeyRound className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#141a28] border border-slate-700/80 focus:border-amber-500 text-slate-100 pl-11 pr-4 py-3 rounded-xl text-sm outline-none transition-colors font-mono"
              />
            </div>
          </div>

          {/* Preset hint */}
          <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20 text-amber-400 text-[11px] font-mono flex items-center justify-between">
            <span>Configured .env Login:</span>
            <span className="font-bold">admin / password</span>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            <Lock className="w-4 h-4" />
            <span>{isSubmitting ? 'Authenticating...' : 'Sign In to Terminal'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
