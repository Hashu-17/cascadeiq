import React from 'react';
import './IncidentTable.css';

const rows = [
  { id: 1, service: 'payment-service', severity: 'HIGH', status: 'ACTIVE' },
  { id: 2, service: 'auth-service', severity: 'LOW', status: 'RESOLVED' },
];

function IncidentTable() {
  return (
    <table className="incident-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Severity</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(row => (
          <tr key={row.id}>
            <td>{row.service}</td>
            <td>{row.severity}</td>
            <td>{row.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default IncidentTable;
