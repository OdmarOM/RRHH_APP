import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
        username,
        password
      });
      
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify({
        username: response.data.username,
        rol: response.data.rol,
        empleado_nombre: response.data.empleado_nombre
      }));
      
      onLogin(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error de autenticación');
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    },
    card: {
      backgroundColor: 'white',
      borderRadius: '20px',
      padding: '40px',
      width: '100%',
      maxWidth: '400px',
      boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
    },
    title: {
      textAlign: 'center',
      fontSize: '28px',
      fontWeight: 'bold',
      marginBottom: '10px',
      color: '#333'
    },
    subtitle: {
      textAlign: 'center',
      color: '#666',
      marginBottom: '30px'
    },
    input: {
      width: '100%',
      padding: '12px',
      marginBottom: '15px',
      border: '2px solid #e0e0e0',
      borderRadius: '8px',
      fontSize: '16px',
      boxSizing: 'border-box'
    },
    button: {
      width: '100%',
      padding: '14px',
      backgroundColor: '#667eea',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer'
    },
    error: {
      backgroundColor: '#fee',
      color: '#c33',
      padding: '10px',
      borderRadius: '8px',
      marginBottom: '15px',
      textAlign: 'center'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.title}>Sistema RRHH</div>
        <div style={styles.subtitle}>Iniciar Sesión</div>
        
        {error && <div style={styles.error}>{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={styles.input}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
            required
          />
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
        
        <div style={{ marginTop: '20px', fontSize: '12px', textAlign: 'center', color: '#999' }}>
          Credenciales de prueba:<br/>
          admin / Admin123!<br/>
          supervisor1 / Sup123!<br/>
          rrhh1 / RRHH123!
        </div>
      </div>
    </div>
  );
}

export default Login;
