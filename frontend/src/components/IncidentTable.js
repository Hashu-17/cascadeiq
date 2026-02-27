import React from 'react';
import './IncidentTable.css';

function IncidentTable({ incidents = [], onSelectIncident }) {
  return (
    <table className="incident-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Severity</th>
          <th>Type</th>
          <th>Status</th>
          <th>Workflow</th>
          <th>Confidence</th>
          <th>Leading Hypothesis</th>
        </tr>
      </thead>
      <tbody>
        {incidents.map(row => (
          <tr
            key={row.incident_id}
            onClick={() => onSelectIncident && onSelectIncident(row)}
            style={{ cursor: onSelectIncident ? 'pointer' : 'default' }}
          >
            <td><strong>{row.service_name}</strong></td>
            <td><span className={`badge severity-${row.severity.toLowerCase()}`}>{row.severity}</span></td>
            <td><code>{row.incident_type || '-'}</code></td>
            <td><span className={`badge status-${row.status.toLowerCase()}`}>{row.status}</span></td>
            <td>{row.workflow_status || 'INITIALIZED'}</td>
            <td>{typeof row.confidence === 'number' ? `${Math.round(row.confidence * 100)}%` : '-'}</td>
            <td>{row.probable_cause || 'Analyzing...'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default IncidentTable;
