import os
from pathlib import Path

# Base backend directory
BASE_DIR = Path(__file__).resolve().parent

# Data directory for storing pickled embeddings
DATA_DIR = BASE_DIR / "data"
ENROLLED_DIR = DATA_DIR / "enrolled"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.pkl"

# Uploads directory for temporary image files
UPLOADS_DIR = BASE_DIR / "uploads"

# Ensure required directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
ENROLLED_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Face recognition match threshold (Euclidean distance)
# Lower distance = closer face match
# Initial default threshold: 0.50
FACE_MATCH_THRESHOLD = 0.50

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
