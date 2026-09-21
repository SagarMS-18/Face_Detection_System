import React from 'react';

export default function Navbar({ healthStatus, personsCount, enrolledList }) {
  const isHealthy = healthStatus && healthStatus.status === 'success';

  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="brand">
          <div className="brand-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 11A7 7 0 0 1 5 11" />
              <circle cx="12" cy="11" r="3" />
              <path d="M12 2v2" />
              <path d="M12 18v4" />
              <path d="M4.93 4.93l1.41 1.41" />
              <path d="M17.66 17.66l1.41 1.41" />
              <path d="M2 12h2" />
              <path d="M20 12h2" />
              <path d="M6.34 17.66l-1.41 1.41" />
              <path d="M19.07 4.93l-1.41 1.41" />
            </svg>
          </div>
          <div>
            <h1 className="brand-title">Face Recognition System</h1>
            <p className="brand-subtitle">AI-based 128-D Face Encoding & Identification</p>
          </div>
        </div>

        <div className="navbar-badges">
          <div className={`status-badge ${isHealthy ? 'healthy' : 'unhealthy'}`}>
            <span className="dot"></span>
            {isHealthy ? 'Backend Active (5000)' : 'Backend Disconnected'}
          </div>

          <div className="count-badge">
            <span className="count-label">Enrolled Persons:</span>
            <span className="count-number">{personsCount}</span>
          </div>
        </div>
      </div>
      
      {enrolledList && enrolledList.length > 0 && (
        <div className="enrolled-pills">
          <span className="pills-title">Database:</span>
          {enrolledList.map((name, idx) => (
            <span key={idx} className="person-pill">{name}</span>
          ))}
        </div>
      )}
    </header>
  );
}
