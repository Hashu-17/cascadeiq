import React, { useEffect, useState } from 'react';
import './App.css';
import IncidentTable from './components/IncidentTable';

function App() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/incidents`)
      .then(res => res.json())
      .then(data => {
        setIncidents(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Unable to load incidents');
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>CascadeIQ</h1>
        {loading && <p>Loading incidents...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && <IncidentTable incidents={incidents} />}
      </header>
    </div>
  );
}

export default App;
