import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function ZebraTerminal() {
  const [status, setStatus] = useState('Cargando...');
  const [gafete, setGafete] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);
  
  const token = localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await axios.get('http://localhost:8000/health');
        if (response.data.status === 'healthy') {
          setStatus('Online');
        } else {
          setStatus('Offline');
        }
      } catch (error) {
        setStatus('Offline');
      }
    };
    
    checkBackend();
    inputRef.current?.focus();
    
    const interval = setInterval(checkBackend, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleEscanear = async () => {
    if (!gafete.trim() || loading) return;

    setLoading(true);
    setError(null);
    setResultado(null);

    try {
      const url = 'http://localhost:8000/api/v1/caseta/escanear/' + gafete;
      const response = await axios.post(url, {}, {
        headers: { Authorization: 'Bearer ' + token }
      });
      setResultado(response.data);

      setTimeout(() => {
        setGafete('');
        inputRef.current?.focus();
      }, 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al procesar el escaneo');
      setTimeout(() => {
        setGafete('');
        inputRef.current?.focus();
      }, 3000);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleEscanear();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.reload();
  };

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
      padding: '20px',
    },
    header: {
      backgroundColor: status === 'Online' ? '#10b981' : '#eab308',
      color: 'black',
      padding: '20px',
      textAlign: 'center',
      fontWeight: 'bold',
      fontSize: '24px',
      marginBottom: '30px',
      borderRadius: '10px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    card: {
      maxWidth: '600px',
      margin: '0 auto',
      backgroundColor: 'white',
      borderRadius: '20px',
      padding: '30px',
      boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)',
    },
    input: {
      width: '100%',
      fontSize: '24px',
      padding: '20px',
      border: '3px solid #d1d5db',
      borderRadius: '10px',
      marginBottom: '20px',
      textAlign: 'center',
      boxSizing: 'border-box',
    },
    button: {
      width: '100%',
      fontSize: '32px',
      padding: '30px',
      backgroundColor: '#eab308',
      color: 'white',
      border: 'none',
      borderRadius: '10px',
      cursor: 'pointer',
      fontWeight: 'bold',
    },
    buttonDisabled: {
      opacity: 0.5,
      cursor: 'not-allowed',
    },
    success: {
      marginTop: '20px',
      padding: '20px',
      backgroundColor: '#dcfce7',
      border: '2px solid #22c55e',
      borderRadius: '10px',
    },
    error: {
      marginTop: '20px',
      padding: '20px',
      backgroundColor: '#fee2e2',
      border: '2px solid #ef4444',
      borderRadius: '10px',
    },
    loading: {
      marginTop: '20px',
      padding: '20px',
      backgroundColor: '#fef3c7',
      border: '2px solid #f59e0b',
      borderRadius: '10px',
      textAlign: 'center',
    },
    logoutBtn: {
      backgroundColor: '#ef4444',
      color: 'white',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '8px',
      cursor: 'pointer',
      fontSize: '16px',
      fontWeight: 'bold'
    },
    userInfo: {
      fontSize: '14px',
      marginTop: '5px'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <div>SISTEMA DE VIGILANCIA - CASETA</div>
          <div style={styles.userInfo}>👤 {user.empleado_nombre || user.username} | API: {status}</div>
        </div>
        <button onClick={handleLogout} style={styles.logoutBtn}>Salir</button>
      </div>

      <div style={styles.card}>
        <h2 style={{ textAlign: 'center', fontSize: '28px', marginBottom: '20px' }}>
          📱 Escanear Gafete
        </h2>

        <input
          ref={inputRef}
          type="text"
          value={gafete}
          onChange={(e) => setGafete(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Número de empleado"
          style={styles.input}
          disabled={loading}
        />

        <button
          onClick={handleEscanear}
          disabled={loading || !gafete.trim() || status === 'Offline'}
          style={{
            ...styles.button,
            ...(loading || !gafete.trim() || status === 'Offline' ? styles.buttonDisabled : {}),
          }}
        >
          {loading ? '⏳ PROCESANDO...' : '✓ ESCANEAR'}
        </button>

        {loading && (
          <div style={styles.loading}>
            <strong>Procesando escaneo...</strong>
          </div>
        )}

        {resultado && (
          <div style={styles.success}>
            <div style={{ fontWeight: 'bold', fontSize: '20px', marginBottom: '10px' }}>
              ✅ {resultado.empleado}
            </div>
            <div style={{ fontSize: '18px', marginBottom: '5px' }}>
              Estado: <strong>{resultado.estado}</strong>
            </div>
            <div style={{ marginTop: '10px', color: '#166534' }}>
              {resultado.mensaje}
            </div>
            {resultado.pase_expira && (
              <div style={{ marginTop: '10px', fontSize: '14px', color: '#b91c1c' }}>
                ⏰ Pase expira: {new Date(resultado.pase_expira).toLocaleTimeString()}
              </div>
            )}
            {resultado.es_retardo && (
              <div style={{ marginTop: '10px', fontSize: '14px', color: '#f59e0b' }}>
                ⚠️ Requiere aprobación del supervisor
              </div>
            )}
          </div>
        )}

        {error && (
          <div style={styles.error}>
            <div style={{ fontWeight: 'bold', fontSize: '18px', marginBottom: '5px' }}>
              ❌ Error
            </div>
            <div>{error}</div>
          </div>
        )}
      </div>

      <div style={{ ...styles.card, marginTop: '20px', backgroundColor: '#f8fafc' }}>
        <h3 style={{ fontSize: '18px', marginBottom: '10px' }}>📋 Instrucciones</h3>
        <ul style={{ margin: 0, paddingLeft: '20px', color: '#475569' }}>
          <li>✓ Escanee el código de barras del gafete</li>
          <li>✓ Presione ENTER o use el botón táctil</li>
          <li>✓ El sistema detecta retardos automáticamente</li>
          <li>✓ Los retardos requieren aprobación del supervisor</li>
        </ul>
      </div>
    </div>
  );
}

export default ZebraTerminal;
