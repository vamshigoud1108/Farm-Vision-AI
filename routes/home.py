from flask import Blueprint, request, render_template
home_bp = Blueprint('home',__name__)

@home_bp.route('/')
def home_page():
  return render_template('home.html')