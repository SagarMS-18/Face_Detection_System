import face_recognition

def generate_face_embedding(image_path):
    """
    Loads an image, detects faces, enforces exactly 1 face, 
    and returns its 128-dimensional face encoding vector.

    Returns:
        (encoding, None) if successful.
        (None, error_message) if validation fails.
    """
    try:
        # Step 1: Load image using face_recognition
        image = face_recognition.load_image_file(image_path)
    except Exception as e:
        return None, f"Failed to read image file: {str(e)}"

    # Step 2: Detect face locations in the image
    face_locations = face_recognition.face_locations(image)
    num_faces = len(face_locations)

    # Step 3: Handle 0 faces
    if num_faces == 0:
        return None, "No face detected in the image."

    # Step 4: Handle multiple faces (> 1)
    if num_faces > 1:
        return None, "Multiple faces detected. Please upload an image containing only one face."

    # Step 5: Generate 128-dimensional encoding for the single detected face
    encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

    if len(encodings) == 0:
        return None, "Could not compute encoding for the detected face."

    # Return the 128-D vector (numpy array)
    return encodings[0], None
