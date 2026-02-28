import React from 'react';

function getAgentMeta(agentName) {
  if (agentName === 'log-agent') {
    return {
      displayName: 'Log Analysis Agent',
      role: 'Signals & Pattern Recognition',
      color: '#38bdf8',
    };
  }
  if (agentName === 'deployment-agent') {
    return {
      displayName: 'Deployment Correlation Agent',
      role: 'Release & Version Analysis',
      color: '#a855f7',
    };
  }
  return {
    displayName: agentName || 'Operational Agent',
    role: 'Autonomous Reasoning',
    color: '#10b981',
  };
}

function AgentReasoningPanel({ hypotheses = [], probableCause, confidence, summary }) {
  if (!hypotheses || hypotheses.length === 0) {
    return (
      <div className="agent-panel empty-card">
        <h4>Multi-Agent Reasoning</h4>
        <p className="subtext">Waiting for agent analysis results...</p>
      </div>
    );
  }

  return (
    <div className="agent-reasoning-container">
      <div className="agent-panel-header">
        <div className="panel-title-group">
          <h4>Multi-Agent Diagnostic Reasoning</h4>
          <span className="badge-pill badge-ai">PHASE 3 ENGINES</span>
        </div>
        {typeof confidence === 'number' && (
          <div className="top-confidence-badge">
            <span className="conf-label">Leading Confidence:</span>
            <span className="conf-value">{Math.round(confidence * 100)}%</span>
          </div>
        )}
      </div>

      {summary && (
        <div className="consensus-summary-box">
          <div className="summary-content">
            <strong>Synthesized Assessment:</strong>
            <p>{summary}</p>
          </div>
        </div>
      )}

      <div className="agent-cards-grid">
        {hypotheses.map((hypo, idx) => {
          const meta = getAgentMeta(hypo.agent_name);
          const confPercent = Math.round((hypo.confidence || 0) * 100);
          const confColorClass =
            confPercent >= 75 ? 'meter-high' : confPercent >= 50 ? 'meter-med' : 'meter-low';

          return (
            <div key={hypo.agent_name || idx} className="agent-card">
              <div className="agent-card-header">
                <div className="agent-title-row">
                  <div>
                    <h5 className="agent-name">{meta.displayName}</h5>
                    <span className="agent-role">{meta.role}</span>
                  </div>
                </div>

                <div className="confidence-meter-container">
                  <span className="confidence-numeric">{confPercent}%</span>
                  <div className="meter-track">
                    <div
                      className={`meter-fill ${confColorClass}`}
                      style={{ width: `${confPercent}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="agent-hypothesis-body">
                <div className="cause-section">
                  <span className="cause-label">Hypothesized Cause</span>
                  <p className="cause-text">{hypo.probable_cause}</p>
                </div>

                {hypo.evidence && hypo.evidence.length > 0 && (
                  <div className="evidence-section">
                    <span className="section-label">Extracted Signals & Evidence:</span>
                    <ul className="evidence-list">
                      {hypo.evidence.map((item, eIdx) => (
                        <li key={eIdx} className="evidence-item">
                          <code>{item}</code>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {hypo.recommendation && (
                  <div className="recommendation-section">
                    <span className="rec-text">{hypo.recommendation}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default AgentReasoningPanel;
