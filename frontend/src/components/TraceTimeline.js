import React from 'react';

function TraceTimeline({ traces = [] }) {
  return <ol className="trace-timeline">{traces.map(trace => <li key={trace.id}>{trace.stage}: {trace.message}</li>)}</ol>;
}

export default TraceTimeline;
