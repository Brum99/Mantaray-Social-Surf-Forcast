from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import mysql.connector
from utils import calculate_distance, get_hemisphere, closest_point
from database import query_all_users
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host='localhost',
        database=Config.DB_NAME
    )
    return connection

# User model class
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, email, password_hash FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def find_by_username(username):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, email, password_hash FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return User(*user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
@login_required
def map_page():
    return render_template('map.html')

@app.route('/closest_point', methods=['GET'])
def closest_point_route():
    try:
        lng = float(request.args.get('lng'))
        lat = float(request.args.get('lat'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid latitude or longitude'}), 400

    result, status_code = closest_point(lng, lat)
    return jsonify(result), status_code

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('map_page'))
        else:
            flash('Invalid username or password. Please try again or sign up.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        existing_user = User.find_by_username(username)
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('sign_up'))

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                       (username, email, password_hash))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('sign_up.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)