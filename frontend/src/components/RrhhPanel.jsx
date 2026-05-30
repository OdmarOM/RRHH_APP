import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RrhhPanel({ user, onLogout }) {
  const [asistencias, setAsistencias] = useState([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');

  useEffect(() => {
    cargarAsistencias();
  }, []);

  const cargarAsistencias = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/rrhh/asistencias', {
        headers: { Authorization: 'Bearer ' + token }
      });
      setAsistencias(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: { minHeight: '100vh', background: '#f5f5f5' },
    header: { background: '#3498db', color: 'white', padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
    content: { padding: '20px', maxWidth: '1200px', margin: '0 auto' },
    card: { background: 'white', borderRadius: '10px', padding: '20px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
    table: { width: '100%', borderCollapse: 'collapse' },
    th: { padding: '12px', textAlign: 'left', borderBottom: '2px solid #ddd', background: '#f8f9fa' },
    td: { padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' },
    logoutBtn: { background: '#e74c3c', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '5px', cursor: 'pointer' }
  };

  const getEstadoColor = (estado) => {
    const colores = {
      'Normal': '#27ae60',
      'Retardo_Aprobado': '#f39c12',
      'Incidencia': '#e74c3c',
      'Visita_Descanso': '#3498db'
    };
    return colores[estado] || '#95a5a6';
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2>Panel de RRHH</h2>
          <small>Bienvenido, {user.empleado_nombre || user.username}</small>
        </div>
        <button onClick={onLogout} style={styles.logoutBtn}>Cerrar Sesión</button>
      </div>

      <div style={styles.content}>
        <div style={styles.card}>
          <h3>📊 Registro de Asistencias</h3>
          {loading ? (
            <p>Cargando...</p>
          ) : (
            <table style={styles.table}>
              <thead>
                <tr><th style={styles.th}>Empleado</th><th style={styles.th}>Fecha</th><th style={styles.th}>Entrada</th><th style={styles.th}>Estado</th></tr>
              </thead>
              <tbody>
                {asistencias.map(reg => (
                  <tr key={reg.id}>
                    <td style={styles.td}>{reg.empleado_nombre}</td>
                    <td style={styles.td}>{new Date(reg.fecha_turno).toLocaleDateString()}</td>
                    <td style={styles.td}>{reg.hora_entrada_real ? new Date(reg.hora_entrada_real).toLocaleTimeString() : 'Pendiente'}</td>
                    <td style={styles.td}><span style={{color: getEstadoColor(reg.estado_registro)}}>{reg.estado_registro}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default RrhhPanel;
