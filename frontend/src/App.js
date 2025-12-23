import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState('loading');

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/health`)
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(err => setStatus('error'));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>CascadeIQ</h1>
        <p>API Status: {status}</p>
      </header>
    </div>
  );
}

export default App;
