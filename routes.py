from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from database import get_db_connection
from utils import closest_point
from weather_service import fetch_and_save_weather_data

def register_routes(app):
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

    @app.route('/save_location', methods=['POST'])
    def save_location():
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        name = data.get('name', 'Unnamed Location')

        if not latitude or not longitude:
            return jsonify({'success': False, 'message': 'Latitude and longitude are required'}), 400

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT location_id FROM locations WHERE latitude = %s AND longitude = %s", (latitude, longitude))
            existing_location = cursor.fetchone()

            if existing_location:
                return jsonify({'success': False, 'message': 'This location already exists', 'location_id': existing_location[0]}), 400

            cursor.execute("INSERT INTO locations (latitude, longitude, name) VALUES (%s, %s, %s)",
                           (latitude, longitude, name))

            connection.commit()
            location_id = cursor.lastrowid
            cursor.close()
            connection.close()

            return jsonify({'success': True, 'message': 'Location saved successfully', 'location_id': location_id})
        except Exception as e:
            print(f"Error saving location: {str(e)}")
            return jsonify({'success': False, 'message': 'An error occurred while saving the location'}), 500

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.find_by_username(username)
            if user and check_password_hash(user.password, password):
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
            password = generate_password_hash(password)

            existing_user = User.find_by_username(username)
            if existing_user:
                flash('Username already exists. Please choose a different one.')
                return redirect(url_for('sign_up'))

            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, password))
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

    @app.route('/fetch_and_save_weather', methods=['POST'])
    def fetch_and_save_weather_route():
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_id = data.get('location_id')

        if not all([latitude, longitude, location_id]):
            return jsonify({'success': False, 'message': 'Latitude, longitude, and location_id are required'}), 400

        result = fetch_and_save_weather_data(latitude, longitude, location_id)
        return jsonify(result)