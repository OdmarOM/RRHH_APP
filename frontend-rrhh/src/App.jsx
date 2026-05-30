import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Componente temporal para la pantalla de Caseta (Zebra)
const CasetaView = () => (
  <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
    <h1 className="text-3xl font-bold text-blue-400 mb-6">Terminal Zebra - Vigilancia</h1>
    <div className="w-full max-w-md bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-700">
      <p className="text-center text-gray-400 mb-4">Esperando escaneo de gafete...</p>
      {/* Aquí irá el input invisible para el escáner y los botones grandes */}
      <input 
        type="text" 
        autoFocus 
        className="w-full p-3 rounded bg-gray-700 text-white border border-gray-600 focus:border-blue-500 outline-none"
        placeholder="Ingrese número de empleado"
      />
    </div>
  </div>
);

// Componente temporal para el panel de RRHH (PC)
const RRHHView = () => (
  <div className="min-h-screen bg-gray-100 flex">
    {/* Menú lateral */}
    <div className="w-64 bg-white shadow-md flex flex-col">
      <div className="p-4 bg-blue-600 text-white font-bold text-xl">Panel RRHH</div>
      <nav className="flex-1 p-4 flex flex-col gap-2">
        <button className="text-left p-2 hover:bg-gray-100 rounded text-gray-700">Asistencias</button>
        <button className="text-left p-2 hover:bg-gray-100 rounded text-gray-700">Empleados</button>
      </nav>
    </div>
    {/* Contenido principal */}
    <div className="flex-1 p-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Dashboard de Asistencias</h1>
      <div className="bg-white p-6 rounded shadow border border-gray-200 h-64 flex items-center justify-center">
        <p className="text-gray-500">Aquí irá la tabla de datos conectada a Python.</p>
      </div>
    </div>
  </div>
);

// Pantalla de inicio para elegir a dónde ir
const Home = () => (
  <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-6">
    <h1 className="text-4xl font-bold text-gray-800">Sistema Central</h1>
    <div className="flex gap-4">
      <Link to="/caseta" className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 font-semibold">
        Entrar como Vigilante
      </Link>
      <Link to="/rrhh" className="px-6 py-3 bg-purple-600 text-white rounded-lg shadow hover:bg-purple-700 font-semibold">
        Entrar como RRHH
      </Link>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/caseta" element={<CasetaView />} />
        <Route path="/rrhh" element={<RRHHView />} />
      </Routes>
    </Router>
  );
}

export default App;