import React, { useState } from 'react';
import { identifyFace } from '../services/api';
import ResultCard from './ResultCard';

export default function Identify() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [identifyResult, setIdentifyResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setErrorMsg(null);
    setIdentifyResult(null);
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handleIdentify = async (e) => {
    e.preventDefault();
    setErrorMsg(null);
    setIdentifyResult(null);

    if (!selectedFile) {
      setErrorMsg('Please select a face image to identify.');
      return;
    }

    setLoading(true);
    const res = await identifyFace(selectedFile);
    setLoading(false);

    if (res.success) {
      setIdentifyResult(res);
    } else {
      setErrorMsg(res.message || 'Identification failed.');
    }
  };

  return (
    <div className="card identify-card">
      <div className="card-header">
        <div className="card-icon identify-icon">🔍</div>
        <div>
          <h2>Identify Face</h2>
          <p>Query image against enrolled face embeddings</p>
        </div>
      </div>

      <form onSubmit={handleIdentify} className="card-form">
        <div className="form-group">
          <label htmlFor="identifyImage">Query Image</label>
          <div className="file-dropzone">
            <input
              id="identifyImage"
              type="file"
              accept="image/png, image/jpeg, image/jpg, image/webp"
              onChange={handleFileChange}
              disabled={loading}
            />
            {previewUrl ? (
              <div className="preview-container">
                <img src={previewUrl} alt="Query Preview" className="image-preview" />
                <span className="file-name">{selectedFile?.name}</span>
              </div>
            ) : (
              <div className="dropzone-prompt">
                <span className="upload-icon">🔍</span>
                <span>Click or drag query image here</span>
                <span className="file-hint">JPG, PNG, WEBP (Single face)</span>
              </div>
            )}
          </div>
        </div>

        <button type="submit" className="btn btn-secondary" disabled={loading}>
          {loading ? (
            <span className="btn-spinner">Matching Encodings...</span>
          ) : (
            'Identify Face'
          )}
        </button>
      </form>

      {errorMsg && (
        <div className="alert-box alert-error">
          <span className="alert-icon">❌</span>
          <p className="alert-text">{errorMsg}</p>
        </div>
      )}

      {identifyResult && <ResultCard result={identifyResult} />}
    </div>
  );
}
