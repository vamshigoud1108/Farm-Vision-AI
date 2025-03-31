from flask import Blueprint, request, render_template
import json
import os
import threading

disease_result_bp = Blueprint('disease_result', __name__)

# Load diseases list from JSON file
try:
    with open('diseases_list.json', 'r') as f:
        disease_data = json.load(f)
except Exception as e:
    print(f"Error loading disease info: {e}")
    disease_data = {}

# Upload Folder
UPLOAD_FOLDER = 'static/uploads'
CONFIDENCE_THRESHOLD = 0.3

@disease_result_bp.route('/', methods=['GET'])
def show_disease_result():
    try:
        disease_name = request.args.get('disease_name', 'Unknown Disease')
        confidence_score = float(request.args.get('confidence', 0))
        print('confidence',confidence_score)
        image_filename = request.args.get('image', None)

        # Initializing image URL
        image_url = None
        if image_filename:
            try:
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                if os.path.exists(image_path):
                    image_url = f"/{image_path}"
                    # Schedule deletion of the image after a short delay (e.g., 60 seconds)
                    threading.Timer(60, lambda: os.remove(image_path) if os.path.exists(image_path) else None).start()
            except Exception as e:
                print(f"Error processing image path: {e}")

        # Normalizing disease names for comparison
        try:
            normalized_disease_data = {key.strip(): value for key, value in disease_data.items()}
        except Exception as e:
            print(f"Error normalizing disease data: {e}")
            return "Error processing disease data", 500

        # Handle low confidence cases
        if confidence_score < CONFIDENCE_THRESHOLD:
            return render_template(
                'disease_result.html',
                disease_name="Uncertain Diagnosis",
                is_healthy=False,
                cause="The model is unsure about this image.",
                cure_steps=["Try uploading a clearer image or consult an expert."],
                image_url=image_url
            )

        # Check if disease exists in data
        if disease_name in normalized_disease_data:
            disease_info = normalized_disease_data[disease_name]

            # If the disease entry contains a "Message," it's a healthy plant
            if "Message" in disease_info:
                return render_template(
                    'disease_result.html',
                    disease_name=disease_name,
                    is_healthy=True,
                    message=disease_info["Message"],
                    image_url=image_url
                )
            # Otherwise, provide disease details
            return render_template(
                'disease_result.html',
                disease_name=disease_name,
                is_healthy=False,
                cause=disease_info.get("Cause", "Cause not available."),
                cure_steps=disease_info.get("Cure_Steps", ["No cure steps available."]),
                image_url=image_url
            )
    except Exception as e:
        print(f"Unexpected error in show_disease_result: {e}")
        return "An unexpected error occurred.", 500

    return render_template('disease_result.html')
