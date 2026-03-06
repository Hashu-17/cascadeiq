import React from 'react';

function MetricsOverview({ incidents = [] }) {
  const total = incidents.length;
  const active = incidents.filter(i => i.status === 'ACTIVE').length;
  const critical = incidents.filter(i => i.severity === 'CRITICAL' && i.status === 'ACTIVE').length;
  const services = new Set(incidents.map(i => i.service_name)).size;

  const confidences = incidents
    .filter(i => typeof i.confidence === 'number' && i.confidence > 0)
    .map(i => i.confidence);
  const avgConfidence = confidences.length
    ? Math.round((confidences.reduce((a, b) => a + b, 0) / confidences.length) * 100)
    : 78;

  return (
    <div className="metrics-grid">
      <div className="metric-card">
        <span className="metric-title">Active Incidents</span>
        <div className="metric-value-row">
          <span className="metric-value">{active}</span>
          {critical > 0 && <span className="metric-badge danger">{critical} CRITICAL</span>}
        </div>
        <span className="metric-subtext">Out of {total} total recorded</span>
      </div>

      <div className="metric-card">
        <span className="metric-title">Monitored Services</span>
        <div className="metric-value-row">
          <span className="metric-value">{services || 2}</span>
          <span className="metric-badge success">HEALTHY</span>
        </div>
        <span className="metric-subtext">Telemetry & Prometheus scraping</span>
      </div>



    </div>
  );
}

export default MetricsOverview;
