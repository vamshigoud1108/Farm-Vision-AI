from flask import Blueprint, request, render_template, redirect, url_for
import joblib
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
disease_bp = Blueprint('disease', __name__)
import uuid
import numpy as np
import os

# Defining folder to store image
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

try:
  # Loading the saved model and class_indices
  model = load_model('models/plant_disease_model.h5')
  model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

  class_indices = joblib.load('models/class_indices.pkl')
  idx_to_class = {v: k for k, v in class_indices.items()}

except Exception as e:
    print(f"ERROR: Failed to load model - {type(e).__name__}: {e}")
    model = None
    idx_to_class = {}

@disease_bp.route('/', methods=['GET','POST'])
def show_disease_form():
  if request.method == 'POST':
      try:
        # Getting the image from the form
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
          print("No selected file")
          return redirect(request.url)
        
        # Generating unique filename and save file
        filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Preprocessing image
        try:
            img = image.load_img(filepath,target_size = (224,224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
          
        except Exception as e:
            print(f"Error processing image: {e}")
            return redirect(request.url)
        
        # Make Prediction
        if model:
            prediction = model.predict(img_array)
            predicted_class_idx = np.argmax(prediction)
            confidence_score = float(np.max(prediction))
            predicted_disease = idx_to_class[predicted_class_idx]
        else:
            print("Error: Model not loaded")
            return redirect(request.url)
        
        return redirect(url_for('disease_result.show_disease_result',disease_name=predicted_disease, image=filename,confidence=confidence_score))
     
      except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect(request.url)  

  return render_template('disease.html')