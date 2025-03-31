import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
from routes.home import home_bp
from routes.crop import crop_bp
from routes.disease import disease_bp
from routes.disease_result import disease_result_bp


app = Flask(__name__)

# Loading environment variables from .env file
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY", "default_fallback_key")

# Registering Blueprints
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(crop_bp, url_prefix='/recommend-crop')
app.register_blueprint(disease_bp, url_prefix='/detect-disease')
app.register_blueprint(disease_result_bp, url_prefix='/disease_result')

# To Serve favicon correctly
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True)