import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Thermometer, Droplets, Heart, AlertTriangle, User, Brain } from 'lucide-react';
import MetricCard from './components/MetricCard';
import HealthChart from './components/HealthChart';

const API_BASE = "http://127.0.0.1:5000/api";

function App() {
  const [telemetry, setTelemetry] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchData = async () => {
    try {
      const [resTel, resHis] = await Promise.all([
        axios.get(`${API_BASE}/telemetry`),
        axios.get(`${API_BASE}/history`)
      ]);
      setTelemetry(resTel.data);
      setHistory(resHis.data);
    } catch (err) {
      console.error("Connection to backend failed");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  if (!telemetry) return <div className="flex h-screen items-center justify-center">Initializing Biosensors...</div>;

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Health Dashboard</h1>
          <p className="text-gray-500">Live Biosensor Telemetry & Diagnostics</p>
        </div>
        <div className="flex items-center space-x-4 bg-white p-3 rounded-lg shadow-sm">
          <User className="text-blue-600" />
          <span className="font-semibold">Patient ID: #8821</span>
        </div>
      </header>

      {/* AI Prediction Banner */}
      <div className={`mb-8 p-4 rounded-lg flex items-center justify-between border-l-4 ${telemetry.prediction === "Stable" ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
        <div className="flex items-center space-x-3">
          <Brain className={telemetry.prediction === "Stable" ? 'text-green-600' : 'text-red-600'} />
          <div>
            <p className="text-sm font-bold uppercase tracking-wider text-gray-600">AI Diagnostic Prediction</p>
            <p className="text-lg font-medium">{telemetry.prediction}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm font-bold text-gray-600">Stress Level</p>
          <span className={`px-3 py-1 rounded-full text-sm font-bold ${telemetry.stress === 'High' ? 'bg-orange-200 text-orange-800' : 'bg-blue-200 text-blue-800'}`}>
            {telemetry.stress}
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard title="Heart Rate" value={telemetry.heart_rate} unit="BPM" icon={Heart} color="bg-red-500" />
        <MetricCard title="Oxygen Level" value={telemetry.spo2} unit="%" icon={Activity} color="bg-blue-500" />
        <MetricCard title="Temperature" value={telemetry.temp} unit="°C" icon={Thermometer} color="bg-yellow-500" />
        <MetricCard title="Blood Glucose" value={telemetry.glucose} unit="mg/dL" icon={Droplets} color="bg-purple-500" />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <HealthChart data={history} dataKey="hr" color="#ef4444" title="Heart Rate" />
        <HealthChart data={history} dataKey="spo2" color="#3b82f6" title="SpO2" />
      </div>
      
      {/* Footer Info */}
      <footer className="mt-8 text-center text-gray-400 text-sm">
        Telemetry updates automatically every 2 seconds via active biosensor simulation.
      </footer>
    </div>
  );
}

export default App;