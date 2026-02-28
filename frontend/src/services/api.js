const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function fetchIncidents() {
  const res = await fetch(`${API_URL}/api/incidents`);
  if (!res.ok) throw new Error('Failed to fetch incidents');
  return res.json();
}

export async function fetchIncident(incidentId) {
  const res = await fetch(`${API_URL}/api/incident/${incidentId}`);
  if (!res.ok) throw new Error('Failed to fetch incident');
  return res.json();
}

export async function simulateIncident(scenario) {
  const res = await fetch(`${API_URL}/api/simulate/${scenario}`, {
    method: 'POST',
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Simulation failed (${res.status})`);
  }
  return res.json();
}

export async function updateIncidentStatus(incidentId, status) {
  const res = await fetch(`${API_URL}/api/incident/${incidentId}/status?status=${encodeURIComponent(status)}`, {
    method: 'PATCH',
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Status update failed (${res.status})`);
  }
  return res.json();
}
