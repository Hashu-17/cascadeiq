import React, { useState } from 'react';
import AgentReasoningPanel from './AgentReasoningPanel';
import TraceTimeline from './TraceTimeline';

function IncidentDetail({ incident, traces = [], loadingTraces = false, onStatusChange }) {
  const [showRawLogs, setShowRawLogs] = useState(true);

  if (!incident) {
    return (
      <div className="incident-detail-empty">
        <div className="empty-selection-box">
          <span className="empty-icon">🎯</span>
          <h3>Select an Incident</h3>
          <p>Choose an active or historical incident from the feed to inspect multi-agent reasoning, evidence, and execution traces.</p>
        </div>
      </div>
    );
  }

  const isResolved = incident.status === 'RESOLVED';
  const severityClass = `badge-sev-${(incident.severity || 'medium').toLowerCase()}`;

  return (
    <div className="incident-detail-panel">
      {/* Top Incident Summary Card */}
      <div className="detail-header-card">
        <div className="detail-header-top">
          <div className="service-title-group">
            <span className={`badge ${severityClass}`}>{incident.severity}</span>
            <h2>{incident.service_name}</h2>
            <span className="incident-type-tag">{incident.incident_type}</span>
          </div>

          <div className="detail-actions">
            <button
              type="button"
              className={`btn btn-toggle-status ${isResolved ? 'btn-reopen' : 'btn-resolve'}`}
              onClick={() => onStatusChange(incident.incident_id, isResolved ? 'ACTIVE' : 'RESOLVED')}
            >
              {isResolved ? '↺ Reopen Incident' : '✓ Resolve Incident'}
            </button>
          </div>
        </div>

        <div className="detail-meta-row">
          <span className="meta-item">
            <strong>ID:</strong> <code>{incident.incident_id}</code>
          </span>
          <span className="meta-item">
            <strong>Workflow:</strong> <code>{incident.workflow_id || 'wf-active'}</code> ({incident.workflow_status || 'TRIAGED'})
          </span>
          <span className="meta-item">
            <strong>Reported:</strong> {new Date(incident.created_at || incident.incident_timestamp).toLocaleString()}
          </span>
        </div>

        {incident.description && (
          <div className="detail-description">
            <p>{incident.description}</p>
          </div>
        )}
      </div>

      {/* Raw Telemetry Terminal */}
      <div className="telemetry-card">
        <div className="telemetry-header" onClick={() => setShowRawLogs(!showRawLogs)}>
          <div className="telemetry-title">
            <span className="console-icon">⌨</span>
            <span>Raw Logs & System Telemetry</span>
          </div>
          <button type="button" className="btn-text-toggle">
            {showRawLogs ? 'Collapse ▲' : 'Expand ▼'}
          </button>
        </div>

        {showRawLogs && (
          <div className="telemetry-body">
            <pre className="log-console-content">
              {incident.raw_logs || 'No raw log data attached to incident.'}
            </pre>
            {incident.incident_metadata && Object.keys(incident.incident_metadata).length > 0 && (
              <div className="metadata-tags">
                <span className="meta-label">Payload Metadata:</span>
                {Object.entries(incident.incident_metadata).map(([k, v]) => (
                  <span key={k} className="meta-pill">
                    {k}: <strong>{String(v)}</strong>
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Multi-Agent Hypotheses Reasoning Section */}
      <AgentReasoningPanel
        hypotheses={incident.hypotheses}
        probableCause={incident.probable_cause}
        confidence={incident.confidence}
        summary={incident.analysis_summary}
      />

      {/* Phase 4 Observability Traces Timeline */}
      <TraceTimeline traces={traces} loading={loadingTraces} />
    </div>
  );
}

export default IncidentDetail;
