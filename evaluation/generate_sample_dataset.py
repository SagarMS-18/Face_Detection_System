import os
import cv2
import numpy as np
from pathlib import Path

# Paths
EVAL_DIR = Path(__file__).resolve().parent
KNOWN_DIR = EVAL_DIR / "known"
UNKNOWN_DIR = EVAL_DIR / "unknown"

# Ensure directories exist
(KNOWN_DIR / "Sagar").mkdir(parents=True, exist_ok=True)
(KNOWN_DIR / "Rahul").mkdir(parents=True, exist_ok=True)
UNKNOWN_DIR.mkdir(parents=True, exist_ok=True)

def create_face_canvas(seed=42):
    """
    Generate a simple face image canvas using OpenCV drawing functions.
    Note: For dlib/face_recognition, real human portrait photos are recommended.
    This script populates sample image paths and placeholder canvas generators.
    """
    np.random.seed(seed)
    canvas = np.zeros((300, 300, 3), dtype=np.uint8)
    canvas[:] = (240, 240, 240)
    
    # Draw head outline
    cv2.ellipse(canvas, (150, 150), (80, 110), 0, 0, 360, (180, 150, 120), -1)
    # Draw eyes
    cv2.circle(canvas, (115, 125), 12, (255, 255, 255), -1)
    cv2.circle(canvas, (185, 125), 12, (255, 255, 255), -1)
    cv2.circle(canvas, (115, 125), 5, (50, 50, 50), -1)
    cv2.circle(canvas, (185, 125), 5, (50, 50, 50), -1)
    # Draw nose
    cv2.line(canvas, (150, 135), (150, 165), (120, 100, 80), 3)
    # Draw mouth
    cv2.ellipse(canvas, (150, 195), (35, 15), 0, 0, 180, (50, 50, 200), 4)

    return canvas

def generate_samples():
    print("Generating sample test directories and structure...")
    
    # Create sample image placeholders if empty
    sagar_img = create_face_canvas(seed=101)
    rahul_img = create_face_canvas(seed=202)
    unknown_img = create_face_canvas(seed=999)

    cv2.imwrite(str(KNOWN_DIR / "Sagar" / "sagar_test1.jpg"), sagar_img)
    cv2.imwrite(str(KNOWN_DIR / "Rahul" / "rahul_test1.jpg"), rahul_img)
    cv2.imwrite(str(UNKNOWN_DIR / "unknown_person1.jpg"), unknown_img)

    print("Sample dataset structure initialized in evaluation/ directory.")

if __name__ == "__main__":
    generate_samples()
