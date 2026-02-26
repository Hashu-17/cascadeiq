import React, { useState, useMemo } from 'react';

function formatTimestamp(ts) {
  if (!ts) return 'just now';
  try {
    const date = new Date(ts);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  } catch {
    return ts;
  }
}

function IncidentFeed({ incidents = [], selectedIncidentId, onSelectIncident }) {
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  const filteredIncidents = useMemo(() => {
    return incidents.filter(incident => {
      // Status/severity tab filter
      if (filter === 'ACTIVE' && incident.status !== 'ACTIVE') return false;
      if (filter === 'RESOLVED' && incident.status !== 'RESOLVED') return false;
      if (filter === 'CRITICAL' && incident.severity !== 'CRITICAL') return false;

      // Text search
      if (search.trim()) {
        const query = search.toLowerCase();
        const matchesService = incident.service_name?.toLowerCase().includes(query);
        const matchesType = incident.incident_type?.toLowerCase().includes(query);
        const matchesDesc = incident.description?.toLowerCase().includes(query);
        const matchesCause = incident.probable_cause?.toLowerCase().includes(query);
        return matchesService || matchesType || matchesDesc || matchesCause;
      }
      return true;
    });
  }, [incidents, filter, search]);

  return (
    <div className="incident-feed-panel">
      <div className="feed-header">
        <div className="feed-title-row">
          <h3>Incident Feed</h3>
          <span className="count-pill">{filteredIncidents.length}</span>
        </div>

        <div className="feed-search-bar">
          <input
            type="text"
            placeholder="Search service, type, or error..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="feed-filter-tabs">
          {['ALL', 'ACTIVE', 'CRITICAL', 'RESOLVED'].map(tab => (
            <button
              key={tab}
              type="button"
              className={`filter-tab ${filter === tab ? 'active' : ''}`}
              onClick={() => setFilter(tab)}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      <div className="feed-list">
        {filteredIncidents.length === 0 ? (
          <div className="feed-empty-state">
            <p>No incidents match the selected filter.</p>
          </div>
        ) : (
          filteredIncidents.map(incident => {
            const isSelected = incident.incident_id === selectedIncidentId;
            const severityClass = `badge-sev-${(incident.severity || 'medium').toLowerCase()}`;
            const statusClass = `badge-status-${(incident.status || 'active').toLowerCase()}`;

            return (
              <div
                key={incident.incident_id}
                className={`incident-card ${isSelected ? 'selected' : ''}`}
                onClick={() => onSelectIncident(incident)}
              >
                <div className="incident-card-top">
                  <span className="incident-service">{incident.service_name}</span>
                  <span className={`badge ${severityClass}`}>{incident.severity}</span>
                </div>

                <div className="incident-card-middle">
                  <span className="incident-type">{incident.incident_type || 'SYSTEM_INCIDENT'}</span>
                  <span className="incident-time">{formatTimestamp(incident.created_at || incident.incident_timestamp)}</span>
                </div>

                <div className="incident-card-bottom">
                  <span className={`badge-pill ${statusClass}`}>{incident.status}</span>
                  <span className="workflow-status-tag">
                    WF: {incident.workflow_status || 'TRIAGED'}
                  </span>
                  {typeof incident.confidence === 'number' && (
                    <span className="confidence-tag">
                      {Math.round(incident.confidence * 100)}% conf
                    </span>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default IncidentFeed;
