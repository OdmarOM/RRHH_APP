import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SupervisorPanel({ user, onLogout }) {
  const [incidencias, setIncidencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mensaje, setMensaje] = useState('');

  const token = localStorage.getItem('token');

  useEffect(() => {
    cargarIncidencias();
  }, []);

  const cargarIncidencias = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/supervisor/incidencias', {
        headers: { Authorization: 'Bearer ' + token }
      });
      setIncidencias(response.data);
    } catch (error) {
      console.error('Error cargando incidencias:', error);
    } finally {
      setLoading(false);
    }
  };

  const aprobarPase = async (asistenciaId) => {
    try {
      await axios.post('http://localhost:8000/api/v1/supervisor/aprobar-pase/' + asistenciaId, {}, {
        headers: { Authorization: 'Bearer ' + token }
      });
      setMensaje('✓ Pase aprobado exitosamente');
      cargarIncidencias();
      setTimeout(() => setMensaje(''), 3000);
    } catch (error) {
      setMensaje(error.response?.data?.detail || 'Error al aprobar');
      setTimeout(() => setMensaje(''), 3000);
    }
  };

  const styles = {
    container: { minHeight: '100vh', background: '#f5f5f5' },
    header: { background: '#2c3e50', color: 'white', padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
    content: { padding: '20px', maxWidth: '1200px', margin: '0 auto' },
    card: { background: 'white', borderRadius: '10px', padding: '20px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
    incidencia: { borderLeft: '4px solid #f39c12', marginBottom: '15px', padding: '15px', background: '#fff9e6' },
    button: { background: '#27ae60', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '5px', cursor: 'pointer' },
    logoutBtn: { background: '#e74c3c', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '5px', cursor: 'pointer' }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2>Panel de Supervisor</h2>
          <small>Bienvenido, {user.empleado_nombre || user.username}</small>
        </div>
        <button onClick={onLogout} style={styles.logoutBtn}>Cerrar Sesión</button>
      </div>

      <div style={styles.content}>
        {mensaje && <div style={{...styles.card, background: '#d4edda', color: '#155724'}}>{mensaje}</div>}
        
        <div style={styles.card}>
          <h3>📋 Incidencias Pendientes de Aprobación</h3>
          {loading ? (
            <p>Cargando...</p>
          ) : incidencias.length === 0 ? (
            <p>✅ No hay incidencias pendientes</p>
          ) : (
            incidencias.map(inc => (
              <div key={inc.id} style={styles.incidencia}>
                <p><strong>Empleado:</strong> {inc.empleado_nombre}</p>
                <p><strong>Fecha:</strong> {new Date(inc.fecha_turno).toLocaleString()}</p>
                <p><strong>Expira:</strong> {inc.pase_expira ? new Date(inc.pase_expira).toLocaleTimeString() : 'N/A'}</p>
                <button onClick={() => aprobarPase(inc.id)} style={styles.button}>
                  Aprobar Pase
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default SupervisorPanel;
