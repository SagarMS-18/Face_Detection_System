from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_utils import allowed_file, save_temp_file, delete_temp_file
from services.face_service import enroll_person, get_enrolled_persons, identify_person

app = Flask(__name__)
# Enable CORS for all routes (allows React frontend on localhost:5173 to connect)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API server status."""
    return jsonify({
        "status": "success",
        "message": "Face Recognition API is running"
    }), 200


@app.route('/api/persons', methods=['GET'])
def list_persons():
    """Endpoint to fetch list of all enrolled persons and image counts."""
    try:
        persons_info = get_enrolled_persons()
        person_names = list(persons_info.keys())
        return jsonify({
            "success": True,
            "persons": person_names,
            "details": persons_info,
            "count": len(person_names)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching persons list: {str(e)}"
        }), 500


@app.route('/api/enroll', methods=['POST'])
def enroll():
    """
    Enroll a new person or add an image to an existing person's face database.
    Expects multipart form data with 'name' and 'image'.
    """
    # 1. Validate request fields
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({"success": False, "message": "Please enter a valid person name."}), 400

    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image file provided in request."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "No image selected for upload."}), 400

    # 2. Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False, 
            "message": "Unsupported file extension. Allowed formats: PNG, JPG, JPEG, WEBP."
        }), 400

    temp_path = None
    try:
        # 3. Save file temporarily
        temp_path = save_temp_file(file)

        # 4. Enroll person via face service
        success, message, number_of_images = enroll_person(name, temp_path)

        if success:
            return jsonify({
                "success": True,
                "person": name,
                "message": message,
                "number_of_images": number_of_images
            }), 200
        else:
            return jsonify({"success": False, "message": message}), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Unexpected server error during enrollment: {str(e)}"
        }), 500
    finally:
        # 5. Clean up temporary uploaded file
        if temp_path:
            delete_temp_file(temp_path)


@app.route('/api/identify', methods=['POST'])
def identify():
    """
    Identify a face from an uploaded query image.
    Expects multipart form data with 'image'.
    """
    # 1. Validate request
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image file provided in request."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "No image selected for identification."}), 400

    # 2. Validate extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Unsupported file extension. Allowed formats: PNG, JPG, JPEG, WEBP."
        }), 400

    temp_path = None
    try:
        # 3. Save file temporarily
        temp_path = save_temp_file(file)

        # 4. Perform face identification
        success, message, result_data = identify_person(temp_path)

        if success:
            return jsonify(result_data), 200
        else:
            return jsonify({"success": False, "message": message}), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Unexpected server error during identification: {str(e)}"
        }), 500
    finally:
        # 5. Clean up temporary file
        if temp_path:
            delete_temp_file(temp_path)


if __name__ == '__main__':
    print("Starting Face Recognition Flask Backend on http://127.0.0.1:5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)
