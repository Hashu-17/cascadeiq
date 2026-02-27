import React from 'react';

function getStageBadge(stage) {
  switch (stage) {
    case 'ingestion':
      return { label: 'INGEST', className: 'badge-stage-ingest' };
    case 'workflow_init':
      return { label: 'INIT', className: 'badge-stage-init' };
    case 'agent_dispatch':
      return { label: 'DISPATCH', className: 'badge-stage-dispatch' };
    case 'agent_execution':
      return { label: 'AGENT EXEC', className: 'badge-stage-agent' };
    case 'triage':
      return { label: 'TRIAGE', className: 'badge-stage-triage' };
    case 'completion':
      return { label: 'RESOLVED', className: 'badge-stage-complete' };
    case 'state_transition':
      return { label: 'STATE CHANGE', className: 'badge-stage-state' };
    default:
      return { label: (stage || 'STEP').toUpperCase(), className: 'badge-stage-default' };
  }
}

function formatTime(timestamp) {
  if (!timestamp) return '';
  try {
    const d = new Date(timestamp);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  } catch {
    return timestamp;
  }
}

function TraceTimeline({ traces = [], loading = false }) {
  if (loading) {
    return (
      <div className="trace-timeline-card loading-state">
        <h5>Execution Trace Timeline</h5>
        <p className="subtext">Loading workflow trace telemetry...</p>
      </div>
    );
  }

  if (!traces || traces.length === 0) {
    return (
      <div className="trace-timeline-card empty-state">
        <div className="trace-header-row">
          <h5>Execution Trace Timeline</h5>
          <span className="badge-pill badge-obs">PHASE 4 OBSERVABILITY</span>
        </div>
        <p className="subtext">No traces recorded yet for this workflow execution.</p>
      </div>
    );
  }

  return (
    <div className="trace-timeline-card">
      <div className="trace-header-row">
        <div>
          <h5>Execution Trace Timeline</h5>
          <span className="subtext">Deterministic audit trail of multi-agent execution</span>
        </div>
        <span className="trace-count-pill">{traces.length} Events</span>
      </div>

      <div className="timeline-container">
        {traces.map((trace, idx) => {
          const badge = getStageBadge(trace.stage);
          const isLast = idx === traces.length - 1;

          return (
            <div key={trace.id || idx} className={`timeline-item ${isLast ? 'timeline-item-last' : ''}`}>
              <div className="timeline-connector">
                <div className={`timeline-node status-${trace.status || 'completed'}`}></div>
                {!isLast && <div className="timeline-line"></div>}
              </div>

              <div className="timeline-content">
                <div className="timeline-item-header">
                  <div className="timeline-stage-group">
                    <span className={`badge-stage ${badge.className}`}>{badge.label}</span>
                    {trace.agent_name && (
                      <span className="agent-tag">@{trace.agent_name}</span>
                    )}
                    {typeof trace.duration_ms === 'number' && trace.duration_ms > 0 && (
                      <span className="duration-tag">{trace.duration_ms}ms</span>
                    )}
                  </div>
                  <span className="timeline-time">{formatTime(trace.timestamp)}</span>
                </div>

                <div className="timeline-message">
                  {trace.message}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default TraceTimeline;
