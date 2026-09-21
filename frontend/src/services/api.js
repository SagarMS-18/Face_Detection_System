const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Check backend health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Server status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return { status: 'error', message: 'Backend unavailable. Please check if Flask server is running.' };
  }
}

/**
 * Get list of enrolled persons and details
 */
export async function getPersons() {
  try {
    const response = await fetch(`${API_BASE_URL}/persons`);
    const data = await response.json();
    return data;
  } catch (error) {
    return { success: false, message: 'Could not connect to backend server.' };
  }
}

/**
 * Enroll a person with name and image file
 * @param {string} name 
 * @param {File} imageFile 
 */
export async function enrollPerson(name, imageFile) {
  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('image', imageFile);

    const response = await fetch(`${API_BASE_URL}/enroll`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    return data;
  } catch (error) {
    return {
      success: false,
      message: 'Failed to connect to backend server. Make sure Flask API is running on http://127.0.0.1:5000.',
    };
  }
}

/**
 * Identify a face from image file
 * @param {File} imageFile 
 */
export async function identifyFace(imageFile) {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${API_BASE_URL}/identify`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    return data;
  } catch (error) {
    return {
      success: false,
      message: 'Failed to connect to backend server. Make sure Flask API is running on http://127.0.0.1:5000.',
    };
  }
}
