import React, { useEffect, useState, useCallback } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import MetricsOverview from './components/MetricsOverview';
import IncidentFeed from './components/IncidentFeed';
import IncidentDetail from './components/IncidentDetail';
import { fetchIncidents, simulateIncident, updateIncidentStatus } from './services/api';
import { fetchWorkflowTraces } from './services/traces';

function App() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncidentId, setSelectedIncidentId] = useState(null);
  const [traces, setTraces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingTraces, setLoadingTraces] = useState(false);
  const [error, setError] = useState(null);
  const [isSimulating, setIsSimulating] = useState(null);

  // Load incidents from backend
  const loadIncidents = useCallback(async (autoSelectFirst = false) => {
    try {
      const data = await fetchIncidents();
      setIncidents(data);
      if (autoSelectFirst && data.length > 0 && !selectedIncidentId) {
        setSelectedIncidentId(data[0].incident_id);
      }
      setError(null);
    } catch (err) {
      setError(err.message || 'Unable to load incidents from server');
    } finally {
      setLoading(false);
    }
  }, [selectedIncidentId]);

  // Initial load
  useEffect(() => {
    loadIncidents(true);
  }, [loadIncidents]);

  // Periodic polling every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadIncidents(false);
    }, 5000);
    return () => clearInterval(interval);
  }, [loadIncidents]);

  // Selected incident object
  const selectedIncident = incidents.find(i => i.incident_id === selectedIncidentId) || (incidents.length > 0 ? incidents[0] : null);

  // Fetch workflow traces whenever the selected incident changes
  useEffect(() => {
    if (selectedIncident?.workflow_id) {
      setLoadingTraces(true);
      fetchWorkflowTraces(selectedIncident.workflow_id)
        .then(traceList => {
          setTraces(traceList);
          setLoadingTraces(false);
        })
        .catch(err => {
          console.warn('Trace load failed:', err);
          setTraces([]);
          setLoadingTraces(false);
        });
    } else {
      setTraces([]);
    }
  }, [selectedIncident?.workflow_id]);

  // Handle simulation trigger
  async function handleSimulate(scenario) {
    setIsSimulating(scenario);
    setError(null);
    try {
      const newIncident = await simulateIncident(scenario);
      setIncidents(prev => [newIncident, ...prev.filter(i => i.incident_id !== newIncident.incident_id)]);
      setSelectedIncidentId(newIncident.incident_id);

      // Immediately fetch its traces
      if (newIncident.workflow_id) {
        setLoadingTraces(true);
        const traceList = await fetchWorkflowTraces(newIncident.workflow_id);
        setTraces(traceList);
        setLoadingTraces(false);
      }
    } catch (err) {
      setError(err.message || `Failed to inject ${scenario}`);
    } finally {
      setIsSimulating(null);
    }
  }

  // Handle incident status toggle (Active <-> Resolved)
  async function handleStatusChange(incidentId, newStatus) {
    try {
      const updated = await updateIncidentStatus(incidentId, newStatus);
      setIncidents(prev =>
        prev.map(item => (item.incident_id === incidentId ? { ...item, status: updated.status } : item))
      );
      if (selectedIncident?.workflow_id) {
        const traceList = await fetchWorkflowTraces(selectedIncident.workflow_id);
        setTraces(traceList);
      }
    } catch (err) {
      setError(err.message || 'Status update failed');
    }
  }

  return (
    <div className="cascadeiq-app">
      <Navbar onSimulate={handleSimulate} isSimulating={isSimulating} />

      <main className="main-content">
        <MetricsOverview incidents={incidents} />

        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠</span>
            <span>{error}</span>
            <button type="button" className="btn-dismiss" onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Connecting to CascadeIQ Incident Mesh...</p>
          </div>
        ) : (
          <div className="workspace-grid">
            <IncidentFeed
              incidents={incidents}
              selectedIncidentId={selectedIncident?.incident_id}
              onSelectIncident={inc => setSelectedIncidentId(inc.incident_id)}
            />

            <IncidentDetail
              incident={selectedIncident}
              traces={traces}
              loadingTraces={loadingTraces}
              onStatusChange={handleStatusChange}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
