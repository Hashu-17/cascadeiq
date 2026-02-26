import React from 'react';

const scenarios = [
  { id: 'api-failure', label: 'API Failure (Redis)', icon: '⚡' },
  { id: 'db-outage', label: 'DB Pool Outage', icon: '💾' },
  { id: 'traffic-spike', label: 'Traffic Surge (Queue)', icon: '📈' },
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
        <div className="system-status-indicator">
          <span className="status-dot pulsing"></span>
          <span className="status-text">CONTROL ROOM ACTIVE</span>
        </div>

        <div className="simulation-actions">
          <span className="simulation-label">Inject Simulation:</span>
          {scenarios.map(({ id, label, icon }) => (
            <button
              key={id}
              type="button"
              className="btn btn-simulate"
              disabled={isSimulating !== null}
              onClick={() => onSimulate(id)}
            >
              <span className="btn-icon">{icon}</span>
              {isSimulating === id ? 'Simulating...' : label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
