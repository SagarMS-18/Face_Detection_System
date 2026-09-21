import os
import pickle
import numpy as np
from config import EMBEDDINGS_FILE, FACE_MATCH_THRESHOLD
from services.embedding_service import generate_face_embedding

def load_database():
    """
    Load stored embeddings dictionary from pickle file.
    Structure: { "PersonName": [array_1, array_2, ...] }
    """
    if not os.path.exists(EMBEDDINGS_FILE):
        return {}
    
    try:
        with open(EMBEDDINGS_FILE, 'rb') as f:
            database = pickle.load(f)
            return database if isinstance(database, dict) else {}
    except Exception as e:
        print(f"Error loading database pickle file: {e}")
        return {}

def save_database(database):
    """
    Save embeddings dictionary to pickle file.
    """
    os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(database, f)

def enroll_person(name, image_path):
    """
    Extract face encoding from image and add to database for specified person name.
    """
    name = name.strip()
    if not name:
        return False, "Person name cannot be empty.", 0

    # Extract 128-D face embedding
    embedding, error_msg = generate_face_embedding(image_path)
    if error_msg:
        return False, error_msg, 0

    # Load existing database
    database = load_database()

    # Append new embedding to person's entry
    if name not in database:
        database[name] = []
    
    database[name].append(embedding)

    # Save updated database back to pickle
    save_database(database)

    image_count = len(database[name])
    return True, "Person enrolled successfully", image_count

def get_enrolled_persons():
    """
    Return dictionary of enrolled persons and their image counts.
    """
    database = load_database()
    persons_info = {}
    for person_name, embeddings_list in database.items():
        persons_info[person_name] = len(embeddings_list)
    return persons_info

def identify_person(image_path):
    """
    Identify a face from query image by calculating minimum Euclidean distance
    against all enrolled embeddings.
    """
    # Extract query embedding
    query_embedding, error_msg = generate_face_embedding(image_path)
    if error_msg:
        return False, error_msg, None

    database = load_database()
    if not database:
        return False, "No enrolled people in the database. Please enroll someone first.", None

    best_match_person = None
    min_distance = float('inf')

    # Compare query embedding with every enrolled embedding
    for person_name, embeddings_list in database.items():
        for stored_embedding in embeddings_list:
            # Calculate Euclidean distance using numpy.linalg.norm
            distance = np.linalg.norm(query_embedding - stored_embedding)
            if distance < min_distance:
                min_distance = distance
                best_match_person = person_name

    min_distance_val = round(float(min_distance), 4)

    # Apply threshold check
    if min_distance <= FACE_MATCH_THRESHOLD:
        return True, "Face identified successfully", {
            "success": True,
            "person": best_match_person,
            "distance": min_distance_val,
            "threshold": FACE_MATCH_THRESHOLD,
            "matched": True
        }
    else:
        return True, "Face rejected as unknown", {
            "success": True,
            "person": "Unknown",
            "distance": min_distance_val,
            "threshold": FACE_MATCH_THRESHOLD,
            "matched": False
        }
