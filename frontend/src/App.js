import React from 'react';
import './App.css';
import IncidentTable from './components/IncidentTable';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>CascadeIQ</h1>
        <IncidentTable />
      </header>
    </div>
  );
}

export default App;

// TODO: add loading and error states
