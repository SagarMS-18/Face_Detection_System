import React from 'react';

export default function ResultCard({ result }) {
  if (!result) return null;

  const isMatched = result.matched;

  return (
    <div className={`result-card ${isMatched ? 'result-matched' : 'result-unknown'}`}>
      <div className="result-header">
        <span className="result-badge">
          {isMatched ? 'MATCH CONFIRMED' : 'REJECTED AS UNKNOWN'}
        </span>
      </div>

      <div className="result-body">
        <div className="result-main-person">
          <span className="person-label">Identified Person</span>
          <span className="person-value">{result.person}</span>
        </div>

        <div className="result-grid">
          <div className="result-stat">
            <span className="stat-label">Euclidean Distance</span>
            <span className="stat-value">{result.distance?.toFixed(4)}</span>
          </div>

          <div className="result-stat">
            <span className="stat-label">Matching Threshold</span>
            <span className="stat-value">{result.threshold?.toFixed(2)}</span>
          </div>

          <div className="result-stat">
            <span className="stat-label">Status</span>
            <span className={`stat-value status-tag ${isMatched ? 'status-matched' : 'status-rejected'}`}>
              {isMatched ? 'Matched' : 'Rejected'}
            </span>
          </div>
        </div>
      </div>

      <div className="result-footer">
        {isMatched ? (
          <p className="result-note success-note">
            ✓ Distance ({result.distance?.toFixed(4)}) ≤ Threshold ({result.threshold?.toFixed(2)}). Match verified.
          </p>
        ) : (
          <p className="result-note rejection-note">
            ⚠️ Distance ({result.distance?.toFixed(4)}) &gt; Threshold ({result.threshold?.toFixed(2)}). Rejected for safety.
          </p>
        )}
      </div>
    </div>
  );
}
