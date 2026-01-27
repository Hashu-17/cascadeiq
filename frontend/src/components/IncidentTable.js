import React from 'react';
import './IncidentTable.css';

function IncidentTable({ incidents }) {
  return (
    <table className="incident-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Severity</th>
          <th>Status</th>
          <th>Workflow</th>
        </tr>
      </thead>
      <tbody>
        {incidents.map(row => (
          <tr key={row.incident_id}>
            <td>{row.service_name}</td>
            <td><span className={`badge severity-${row.severity.toLowerCase()}`}>{row.severity}</span></td>
            <td><span className={`badge status-${row.status.toLowerCase()}`}>{row.status}</span></td>
            <td>{row.workflow_status || 'INITIALIZED'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default IncidentTable;
