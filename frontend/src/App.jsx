import React, { useState, useEffect } from 'react';
import LandingPage from './landing/LandingPage';
import LoginPage from './auth/LoginPage';
import DashboardPage from './dashboard/DashboardPage';

export default function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'login' | 'dashboard'

  useEffect(() => {
    // Check if user is already authenticated
    const savedUser = localStorage.getItem('orion_auth_user');
    if (savedUser) {
      setCurrentView('dashboard');
    }
  }, []);

  const handleLoginSuccess = () => {
    setCurrentView('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('orion_auth_user');
    setCurrentView('landing');
  };

  if (currentView === 'login') {
    return (
      <LoginPage 
        onLoginSuccess={handleLoginSuccess}
        onBackToLanding={() => setCurrentView('landing')}
      />
    );
  }

  if (currentView === 'dashboard') {
    return (
      <DashboardPage 
        onLogout={handleLogout}
      />
    );
  }

  // Default: Landing Page
  return (
    <LandingPage 
      onOpenLogin={() => setCurrentView('login')}
      onLaunchGuest={() => setCurrentView('login')}
    />
  );
}
