import React, { useState } from 'react';
import { enrollPerson } from '../services/api';

export default function Enroll({ onEnrollmentSuccess }) {
  const [name, setName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [responseMsg, setResponseMsg] = useState(null); // { type: 'success' | 'error', text: '', count?: number }

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setResponseMsg(null);
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseMsg(null);

    // Validation cases
    if (!name.trim()) {
      setResponseMsg({ type: 'error', text: 'Please enter a person name.' });
      return;
    }

    if (!selectedFile) {
      setResponseMsg({ type: 'error', text: 'Please select an image file.' });
      return;
    }

    setLoading(true);

    const res = await enrollPerson(name.trim(), selectedFile);
    setLoading(false);

    if (res.success) {
      setResponseMsg({
        type: 'success',
        text: `Successfully enrolled ${res.person}!`,
        count: res.number_of_images
      });
      // Clear file preview and name after successful enrollment
      setSelectedFile(null);
      setPreviewUrl(null);
      if (onEnrollmentSuccess) onEnrollmentSuccess();
    } else {
      setResponseMsg({
        type: 'error',
        text: res.message || 'Enrollment failed.'
      });
    }
  };

  return (
    <div className="card enroll-card">
      <div className="card-header">
        <div className="card-icon enroll-icon">➕</div>
        <div>
          <h2>Enroll Person</h2>
          <p>Add a face embedding to the database</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="card-form">
        <div className="form-group">
          <label htmlFor="personName">Person Name</label>
          <input
            id="personName"
            type="text"
            className="text-input"
            placeholder="e.g. Sagar"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="enrollImage">Face Image</label>
          <div className="file-dropzone">
            <input
              id="enrollImage"
              type="file"
              accept="image/png, image/jpeg, image/jpg, image/webp"
              onChange={handleFileChange}
              disabled={loading}
            />
            {previewUrl ? (
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="image-preview" />
                <span className="file-name">{selectedFile?.name}</span>
              </div>
            ) : (
              <div className="dropzone-prompt">
                <span className="upload-icon">📷</span>
                <span>Click or drag image to upload</span>
                <span className="file-hint">JPG, PNG, WEBP (Single face)</span>
              </div>
            )}
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? (
            <span className="btn-spinner">Processing Face...</span>
          ) : (
            'Enroll Person'
          )}
        </button>
      </form>

      {responseMsg && (
        <div className={`alert-box alert-${responseMsg.type}`}>
          <span className="alert-icon">{responseMsg.type === 'success' ? '✅' : '❌'}</span>
          <div>
            <p className="alert-text">{responseMsg.text}</p>
            {responseMsg.count !== undefined && (
              <p className="alert-subtext">Total stored images for this person: <strong>{responseMsg.count}</strong></p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
