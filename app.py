from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import User
from routes import register_routes

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
