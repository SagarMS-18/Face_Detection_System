import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Enroll from './components/Enroll';
import Identify from './components/Identify';
import { checkHealth, getPersons } from './services/api';
import './App.css';

export default function App() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [personsData, setPersonsData] = useState({ persons: [], count: 0, details: {} });

  const refreshBackendData = async () => {
    const health = await checkHealth();
    setHealthStatus(health);

    const persons = await getPersons();
    if (persons.success) {
      setPersonsData(persons);
    }
  };

  useEffect(() => {
    refreshBackendData();
    // Periodically poll backend status every 10 seconds
    const interval = setInterval(refreshBackendData, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-layout">
      <Navbar
        healthStatus={healthStatus}
        personsCount={personsData.count}
        enrolledList={personsData.persons}
      />

      <main className="main-content">
        <div className="dashboard-grid">
          <Enroll onEnrollmentSuccess={refreshBackendData} />
          <Identify />
        </div>
      </main>

      <footer className="footer">
        <p>Face Recognition Identification System &bull; 128-D Euclidean Vector Matching</p>
      </footer>
    </div>
  );
}
