const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function fetchIncidents() {
  const res = await fetch(`${API_URL}/api/incidents`);
  if (!res.ok) {
    throw new Error('Failed to fetch incidents');
  }
  return res.json();
}

export async function simulateIncident(scenario) {
  const res = await fetch(`${API_URL}/api/simulate/${scenario}`, {
    method: 'POST',
  });
  if (!res.ok) {
    throw new Error(`Failed to simulate ${scenario}`);
  }
  return res.json();
}
