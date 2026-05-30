import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { api } from './api';

// ==========================================
// PANTALLA: CASETA ZEBRA
// ==========================================
const CasetaView = () => {
  const [codigo, setCodigo] = useState('');
  const [mensaje, setMensaje] = useState(null);
  const [empleadoActivo, setEmpleadoActivo] = useState(null);

  const manejarEscaneo = async (e) => {
    e.preventDefault();
    setMensaje(null);
    try {
      const res = await api.post(`/caseta/empleados/escanear/${codigo}`);
      setEmpleadoActivo(res.data);
      setCodigo('');
    } catch (err) {
      setMensaje("❌ " + (err.response?.data?.detail || "Error al escanear"));
      setCodigo('');
    }
  };

  const accionCaseta = async (ruta, body = {}) => {
    try {
      const res = await api.post(ruta, body);
      setMensaje("✅ " + res.data.mensaje);
      setEmpleadoActivo(null); // Limpiar pantalla tras acción
    } catch (err) {
      setMensaje("❌ " + (err.response?.data?.detail || "Error en la operación"));
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-blue-400 mb-6">Operación Caseta</h1>
      <div className="w-full max-w-md bg-gray-800 p-6 rounded shadow border border-gray-700">
        
        {!empleadoActivo ? (
          <form onSubmit={manejarEscaneo}>
            <p className="text-gray-400 mb-2">Escáner de Gafete:</p>
            <input type="text" autoFocus value={codigo} onChange={(e) => setCodigo(e.target.value)}
              className="w-full p-3 rounded bg-gray-700 text-white outline-none mb-4" placeholder="Gafete..." />
            <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded font-bold">Identificar</button>
          </form>
        ) : (
          <div className="text-center">
            <h2 className="text-2xl font-bold text-white mb-2">{empleadoActivo.nombre_completo}</h2>
            <p className="text-gray-400 mb-4">Estado actual: <span className="font-bold text-blue-300">{empleadoActivo.estado_actual}</span></p>
            
            <div className="grid grid-cols-2 gap-3">
              {empleadoActivo.estado_actual === 'Fuera' && (
                <button onClick={() => accionCaseta(`/caseta/empleados/entrada/${empleadoActivo.id}`)} 
                  className="col-span-2 bg-green-600 p-3 rounded font-bold hover:bg-green-700">Registrar Entrada</button>
              )}
              {empleadoActivo.estado_actual === 'Adentro' && (
                <>
                  <button onClick={() => accionCaseta(`/caseta/empleados/salida-temporal`, { empleado_id: empleadoActivo.id, tipo_salida: 'Mandado_Trabajo' })} 
                    className="bg-yellow-600 p-3 rounded font-bold hover:bg-yellow-700">Mandado</button>
                  <button onClick={() => accionCaseta(`/caseta/empleados/salida-temporal`, { empleado_id: empleadoActivo.id, tipo_salida: 'Permiso_Personal' })} 
                    className="bg-orange-600 p-3 rounded font-bold hover:bg-orange-700">Permiso</button>
                  <button onClick={() => accionCaseta(`/caseta/empleados/salida-final/${empleadoActivo.id}`)} 
                    className="col-span-2 bg-red-600 p-3 rounded font-bold hover:bg-red-700">Fin de Turno</button>
                </>
              )}
              {empleadoActivo.estado_actual === 'En_Espera_Pase' && (
                <p className="col-span-2 text-red-400 font-bold">El empleado debe traer firma de supervisor para entrar.</p>
              )}
            </div>
            <button onClick={() => setEmpleadoActivo(null)} className="mt-4 text-gray-500 underline">Cancelar</button>
          </div>
        )}
        
        {mensaje && <div className="mt-4 p-3 bg-gray-700 border border-gray-600 rounded text-center">{mensaje}</div>}
      </div>
      <Link to="/" className="mt-8 text-gray-500 hover:text-white underline">Menú Principal</Link>
    </div>
  );
};

// ==========================================
// PANTALLA: PANEL DEL SUPERVISOR
// ==========================================
const SupervisorView = () => {
  const [incidencias, setIncidencias] = useState([]);
  const [mensaje, setMensaje] = useState("");

  const cargarIncidencias = async () => {
    try {
      const res = await api.get('/supervisor/incidencias');
      setIncidencias(res.data);
    } catch (err) { console.error(err); }
  };

  useEffect(() => { cargarIncidencias(); }, []);

  const aprobar = async (id) => {
    try {
      await api.post(`/supervisor/aprobar-pase/${id}`);
      setMensaje("Pase aprobado exitosamente.");
      cargarIncidencias();
    } catch (err) {
      setMensaje("❌ " + (err.response?.data?.detail || "Error al aprobar"));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Panel de Supervisor</h1>
        <Link to="/" className="text-blue-600 underline">Volver</Link>
      </div>
      {mensaje && <div className="mb-4 p-3 bg-blue-100 text-blue-700 rounded">{mensaje}</div>}
      
      <div className="bg-white p-6 rounded shadow border border-gray-200">
        <h2 className="text-xl font-bold text-red-600 mb-4">Personal en Caseta esperando pase</h2>
        <table className="w-full text-left">
          <thead><tr className="bg-gray-100"><th className="p-3">Empleado</th><th className="p-3">Límite Pase</th><th className="p-3">Acción</th></tr></thead>
          <tbody>
            {incidencias.length === 0 ? <tr><td colSpan="3" className="p-3 text-center">Nadie en espera.</td></tr> : 
              incidencias.map(inc => (
                <tr key={inc.id} className="border-b">
                  <td className="p-3 font-bold">{inc.empleado_id} (Ver Nombre en DB)</td>
                  <td className="p-3 font-mono text-red-500">{new Date(inc.pase_espera_expira).toLocaleTimeString()}</td>
                  <td className="p-3"><button onClick={() => aprobar(inc.id)} className="bg-green-600 text-white px-4 py-2 rounded">Firmar Pase Digital</button></td>
                </tr>
              ))
            }
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ==========================================
// MENÚ PRINCIPAL
// ==========================================
const Home = () => (
  <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center gap-6">
    <h1 className="text-4xl font-bold text-gray-800">Sistema RRHH y Vigilancia</h1>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Link to="/caseta" className="px-6 py-4 bg-slate-800 text-white rounded shadow text-center font-bold">Terminal Zebra</Link>
      <Link to="/supervisor" className="px-6 py-4 bg-orange-600 text-white rounded shadow text-center font-bold">Panel Supervisor</Link>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/caseta" element={<CasetaView />} />
        <Route path="/supervisor" element={<SupervisorView />} />
      </Routes>
    </Router>
  );
}

export default App;