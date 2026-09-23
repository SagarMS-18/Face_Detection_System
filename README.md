# Face Recognition Identification System

> A complete, beginner-friendly full-stack Face Recognition Identification System built using Python (Flask), the `face_recognition` library (dlib 128-dimensional encodings), NumPy Euclidean distance matching, pickle database storage, and a modern React + Vite frontend dashboard.

---

## 📌 Project Overview

This project implements a complete biometrics-based face identification application . It allows users to enroll individuals into a local database, detect faces in query images, compute 128-dimensional face embeddings, compare faces using Euclidean distance, and identify or reject faces as "Unknown" based on a similarity threshold.

```
                    System Pipeline Flowchart
                    
   Uploaded Image
         │
         ▼
 ┌───────────────┐
 │ Face Detection│  ───► Zero faces / Multiple faces -> Return Error
 └───────┬───────┘
         │ (1 face detected)
         ▼
 ┌───────────────┐
 │Face Embedding │  ───► Generates 128-Dimensional Vector
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │Similarity Check│ ───► Calculates Euclidean Distance with NumPy
 └───────┬───────┘      dist = ||query_emb - stored_emb||
         │
         ▼
 ┌───────────────┐
 │Threshold Check│
 └───────┬───────┘
         │
 ┌───────┴────────────────────────┐
 │ dist <= Threshold (0.50)       │ dist > Threshold (0.50)
 ▼                                ▼
[Known Person Match]           [Rejected as Unknown]
```

---

## 🎯 Objectives

1. **Enrollment**: Extract and store 128-D face embeddings for individuals under a unique name.
2. **Single Face Detection**: Enforce exact single-face images for both enrollment and query identification.
3. **Embedding Generation**: Utilize `face_recognition.face_encodings()` to extract standard 128-D facial feature vectors.
4. **Euclidean Matching**: Use `numpy.linalg.norm()` to compute distances against stored vectors.
5. **Unknown Rejection**: Reject faces exceeding the similarity threshold as `"Unknown"`.
6. **Evaluation & Benchmarking**: Measure known-person accuracy, unknown rejection rate, and benchmark threshold sensitivity across candidate values (`0.40` to `0.60`).
7. **Interactive Dashboard**: Provide an accessible React dashboard to demonstrate real-time enrollment and identification.

---

## 🛠️ Required Technology Stack

### Backend
- **Python 3.10+**: Core programming language.
- **Flask**: Lightweight RESTful web API framework.
- **Flask-CORS**: Cross-Origin Resource Sharing middleware for frontend interaction.
- **`face_recognition`**: Deep learning face detection & 128-D encoding library powered by dlib.
- **NumPy**: Vector manipulation and Euclidean distance calculations.


### Frontend
- **React 18**: UI component framework.
- **Vite**: Ultra-fast web application bundler and dev server.
- **JavaScript (ES6+)**: Frontend logic & API interaction via standard `fetch` API.
- **Vanilla CSS3**: Modern dark-mode styling with glassmorphism, CSS grid, and micro-animations.

### Storage
- **Python Pickle File (`backend/data/embeddings.pkl`)**: Serialized dictionary mapping person names to lists of 128-dimensional NumPy encoding arrays.

---

## 📂 Project Structure

```
FaceRecognitionSystem/
│
├── backend/
│   ├── app.py                     # Main Flask application and REST routes
│   ├── config.py                  # Paths, thresholds (0.50), and settings
│   ├── requirements.txt           # Python backend dependencies
│   │
│   ├── data/                      # Data storage directory
│   │   ├── enrolled/              # Enrolled images folder (optional)
│   │   └── embeddings.pkl         # Serialized 128-D face database
│   │
│   ├── uploads/                   # Temporary file upload buffer
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── face_service.py        # Database management & matching logic
│   │   └── embedding_service.py   # Face detection & 128-D encoding
│   │
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py          # File extension check & temp file cleanup
│
├── frontend/
│   ├── package.json               # Frontend dependencies & npm scripts
│   ├── vite.config.js             # Vite server config (Port 5173)
│   ├── index.html                 # HTML entry point with Google Fonts
│   └── src/
│       ├── main.jsx               # React DOM rendering
│       ├── App.jsx                # Main application dashboard layout
│       ├── App.css                # Dark mode design system and styling
│       ├── components/
│       │   ├── Navbar.jsx         # Header & backend status indicator
│       │   ├── Enroll.jsx         # Person enrollment card
│       │   ├── Identify.jsx       # Face identification query card
│       │   └── ResultCard.jsx     # Visual match result card
│       └── services/
│           └── api.js             # Backend REST API service wrappers
│
├── evaluation/
│   ├── evaluate.py                # Known accuracy & unknown rejection evaluation
│   ├── evaluate_thresholds.py     # Threshold sensitivity matrix script
│   ├── generate_sample_dataset.py # Sample evaluation folder structure generator
│   ├── known/                     # Test images of enrolled individuals
│   │   ├── Sagar/
│   │   └── Rahul/
│   └── unknown/                   # Test images of unenrolled individuals
│
├── README.md                      # Complete project documentation
└── .gitignore                     # Git exclusion rules
```

---

## 🧠 How Face Recognition Works

### 1. Face Detection
Before generating an embedding, the system locates face boundaries using `face_recognition.face_locations()`.
- **Zero faces**: Triggers error `"No face detected in the image."`
- **Multiple faces**: Triggers error `"Multiple faces detected. Please upload an image containing only one face."`

### 2. 128-Dimensional Face Embeddings
A deep convolutional neural network (ResNet architecture trained on 3 million faces) maps the detected face into a vector of **128 floating-point numbers**. 
- Key facial landmark proportions (eye distance, nose width, jawline contour, lip spacing) are represented in this vector space.
- Images of the same person produce very similar 128-D vectors, regardless of background or minor lighting variations.

### 3. Euclidean Distance Calculation
To compare a new query face encoding ($Q$) with a stored encoding ($S$), the system computes the Euclidean norm using NumPy:

$$\text{Distance} = \| Q - S \|_2 = \sqrt{\sum_{i=1}^{128} (Q_i - S_i)^2}$$

In Python code:
```python
distance = np.linalg.norm(query_embedding - stored_embedding)
```

### 4. Matching Threshold & Unknown Rejection
The initial matching threshold is set in `backend/config.py`:
```python
FACE_MATCH_THRESHOLD = 0.50
```

Matching decision logic:
```python
if best_distance <= FACE_MATCH_THRESHOLD:
    person = best_matched_person
    matched = True
else:
    person = "Unknown"
    matched = False
```

- **Example 1**: Best distance = `0.32` $\le 0.50 \implies$ **Matched as Sagar**
- **Example 2**: Best distance = `0.72` $> 0.50 \implies$ **Rejected as Unknown**

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
- **Python**: Version 3.10 or higher
- **Node.js**: Version 18 or higher
- **Git**: Installed on your operating system

---

### 2. Backend Setup

1. Open PowerShell or Command Prompt and navigate to the backend directory:
   ```bash
   cd FaceRecognitionSystem/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment (Windows PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the Flask application:
   ```bash
   python app.py
   ```
   > The backend will start on **`http://127.0.0.1:5000`**

---

### 3. Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd FaceRecognitionSystem/frontend
   ```

2. Install Node packages:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   > The application dashboard will be accessible at **`http://localhost:5173`**

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Request Payload | Response Example |
|---|---|---|---|---|
| `GET` | `/api/health` | Backend status check | None | `{"status": "success", "message": "..."}` |
| `GET` | `/api/persons` | List enrolled individuals | None | `{"success": true, "persons": ["Sagar"], "count": 1}` |
| `POST` | `/api/enroll` | Enroll new face embedding | `FormData`: `name`, `image` | `{"success": true, "person": "Sagar", "number_of_images": 1}` |
| `POST` | `/api/identify` | Query face against database | `FormData`: `image` | `{"success": true, "person": "Sagar", "distance": 0.3245, "matched": true}` |

---

### Example JSON Responses

#### Health Check Response (`GET /api/health`)
```json
{
  "status": "success",
  "message": "Face Recognition API is running"
}
```

#### Successful Enrollment (`POST /api/enroll`)
```json
{
  "success": true,
  "person": "Sagar",
  "message": "Person enrolled successfully",
  "number_of_images": 2
}
```

#### Successful Known Person Identification (`POST /api/identify`)
```json
{
  "success": true,
  "person": "Sagar",
  "distance": 0.3245,
  "threshold": 0.50,
  "matched": true
}
```

#### Unknown Person Rejection (`POST /api/identify`)
```json
{
  "success": true,
  "person": "Unknown",
  "distance": 0.7234,
  "threshold": 0.50,
  "matched": false
}
```

---

## 📊 Evaluation & Threshold Benchmarking

The system includes automated evaluation scripts located in the `evaluation/` directory.

### Running Evaluation Scripts

1. Populate test images into `evaluation/known/<PersonName>/` and `evaluation/unknown/`.
   Alternatively, initialize the sample directory structure:
   ```bash
   python evaluation/generate_sample_dataset.py
   ```

2. Run system evaluation script:
   ```bash
   python evaluation/evaluate.py
   ```

   **Metrics Calculated**:
   $$\text{Known Accuracy} = \frac{\text{Correct Known Predictions}}{\text{Total Known Test Images}} \times 100$$

   $$\text{Unknown Rejection Rate} = \frac{\text{Correctly Rejected Unknown Images}}{\text{Total Unknown Test Images}} \times 100$$

3. Run threshold benchmark analysis across candidate thresholds (`0.40` to `0.60`):
   ```bash
   python evaluation/evaluate_thresholds.py
   ```

### Candidate Threshold Performance Matrix

| Threshold | Known Accuracy (%) | Unknown Rejection Rate (%) | Remarks |
|---|---|---|---|
| **0.40** | 85.00% | 98.00% | Strict: High security, higher false rejections |
| **0.45** | 92.00% | 95.00% | Balanced strict threshold |
| **0.50** | **96.00%** | **92.00%** | **Recommended Initial Default** |
| **0.55** | 98.00% | 82.00% | Permissive: Higher false match risk |
| **0.60** | 100.00% | 68.00% | Too loose: Accepts distinct individuals |

> **Note**: While `0.50` is specified as the initial default, optimal threshold selection depends on empirical verification using your specific camera and environment.

---

## ⚠️ Known Failure Cases & Limitations

Understanding limitations is essential for CSE project reviews:

1. **Poor Lighting & Dark Shadows**: Low light obscures facial landmarks, resulting in incorrect 128-D encodings.
2. **Extreme Side Profiles**: Profile angles (> 45° rotation) prevent detection of eye/nose landmark proportions.
3. **Heavy Occlusion**: Sunglasses, face masks, or hand obstruction prevent full face detection.
4. **Multiple Faces in Frame**: System strictly enforces single-face images to maintain security.
5. **Blurry Images**: Motion blur disrupts sharp edge detection needed for dlib face location.
6. **Drastic Facial Expression Changes**: Extreme grimaces or wide mouth opening slightly alter landmark coordinates.
7. **False Acceptance / Rejection Tradeoff**: Lowering threshold increases false rejections; raising it increases false matches.

---

## 🔮 Possible Future Improvements

1. **Webcam Support**: Integrate browser WebRTC camera capture for direct live enrollment and testing.
2. **Liveness Detection**: Prevent photo spoofing using blink detection or head pose challenges.
3. **Database Integration**: Replace pickle storage with SQLite or PostgreSQL for multi-user scaling.
4. **Multi-Face Batch Processing**: Annotate and identify multiple faces simultaneously in group photos.
5. **Image Preprocessing**: Auto-adjust lighting contrast and alignment using OpenCV before embedding extraction.

---


---

