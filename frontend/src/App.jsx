import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import SupervisorPanel from './components/SupervisorPanel';
import RrhhPanel from './components/RrhhPanel';
import ZebraTerminal from './ZebraTerminal';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  // Si no hay usuario, mostrar login
  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  // Redirigir según el rol
  switch (user.rol) {
    case 'Vigilante':
      return <ZebraTerminal />;
    case 'Supervisor':
      return <SupervisorPanel user={user} onLogout={handleLogout} />;
    case 'RRHH':
      return <RrhhPanel user={user} onLogout={handleLogout} />;
    default:
      return <SupervisorPanel user={user} onLogout={handleLogout} />;
  }
}

export default App;
