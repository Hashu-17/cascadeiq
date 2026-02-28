import React from 'react';

const scenarios = [
  { id: 'api-failure', label: 'API Failure (Redis)' },
  { id: 'db-outage', label: 'DB Pool Outage' },
  { id: 'traffic-spike', label: 'Traffic Surge (Queue)' },
];

function Navbar({ onSimulate, isSimulating }) {
  return (
    <header className="navbar">
      <div className="navbar-brand">
        <div className="brand-logo">CIQ</div>
        <div className="brand-info">
          <h2>CascadeIQ</h2>
          <span className="brand-subtitle">AI Incident Orchestration & Telemetry</span>
        </div>
      </div>

      <div className="navbar-controls">
        <div className="simulation-actions">
          <span className="simulation-label">Inject Simulation:</span>
          {scenarios.map(({ id, label }) => (
            <button
              key={id}
              type="button"
              className="btn btn-simulate"
              disabled={isSimulating !== null}
              onClick={() => onSimulate(id)}
            >
              {isSimulating === id ? 'Simulating...' : label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
