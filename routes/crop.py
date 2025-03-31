from flask import Blueprint, request, render_template, redirect, url_for, session
import joblib
crop_bp = Blueprint('crop',__name__)

# Loading the model, scaler and label classes
model = joblib.load('models/crop_recommendation_model.pkl')
scaler = joblib.load('models/scaler.pkl')
label_classes = joblib.load('models/label_classes.pkl')

@crop_bp.route('/', methods=['GET','POST'])
def show_crop_recommendation():
  if request.method == 'POST':
    try:
      # Getting the input values from the form
      Nitrogen = float(request.form['N'])
      Phosphorus = float(request.form['P'])
      Potassium = float(request.form['K'])
      Temperature = float(request.form['temperature'])
      Humidity = float(request.form['humidity'])
      pH = float(request.form['ph'])
      Rainfall = float(request.form['rainfall'])

      # Features
      features = [[
        Nitrogen,
        Phosphorus,
        Potassium,
        Temperature,
        Humidity,
        pH,
        Rainfall
      ]]

      # Feature Scaling
      input_scaled = scaler.transform(features)

      # Predicting crop (numerical label)
      predicted_label = model.predict(input_scaled)[0]

      # Converting label to crop name
      predicted_crop = label_classes[predicted_label]

      session['prediction'] = f'Recommended Crop: <span style="color: #FF8C00; font-weight:600">{predicted_crop.title()}</span>'
      return redirect(url_for('crop.show_crop_recommendation'))
    
    except Exception as e:
      return f"Error: {str(e)}"
  
  prediction = session.pop('prediction', None)
  return render_template('crop.html', prediction = prediction)