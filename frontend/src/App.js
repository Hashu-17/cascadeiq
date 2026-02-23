import React, { useEffect, useState } from 'react';
import './App.css';
import IncidentTable from './components/IncidentTable';
import { fetchIncidents, simulateIncident } from './services/api';

const scenarios = [
  ['api-failure', 'Simulate API Failure'],
  ['db-outage', 'Simulate DB Outage'],
  ['traffic-spike', 'Simulate Traffic Spike'],
];

function App() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeScenario, setActiveScenario] = useState(null);

  useEffect(() => {
    fetchIncidents()
      .then(data => {
        setIncidents(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Unable to load incidents');
        setLoading(false);
      });
  }, []);

  async function handleSimulation(scenario) {
    setActiveScenario(scenario);
    setError(null);
    try {
      const incident = await simulateIncident(scenario);
      setIncidents(current => [incident, ...current]);
    } catch (simulationError) {
      setError(simulationError.message);
    } finally {
      setActiveScenario(null);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>CascadeIQ</h1>
        <div className="simulation-controls">
          {scenarios.map(([scenario, label]) => (
            <button
              key={scenario}
              type="button"
              disabled={activeScenario !== null}
              onClick={() => handleSimulation(scenario)}
            >
              {activeScenario === scenario ? 'Creating...' : label}
            </button>
          ))}
        </div>
        {loading && <p>Loading incidents...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && <IncidentTable incidents={incidents} />}
      </header>
    </div>
  );
}

export default App;
