from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import mysql.connector
from utils import calculate_distance, get_hemisphere, closest_point
from database import query_all_users
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash

from flask import request, jsonify
import pandas as pd
import arrow
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os

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
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, username, email, password FROM users WHERE user_id = %s", (user_id,))
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
        cursor.execute("SELECT user_id, username, email, password FROM users WHERE username = %s", (username,))
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
        # Check if location already exists
        cursor.execute("SELECT location_id FROM locations WHERE latitude = %s AND longitude = %s", (latitude, longitude))
        existing_location = cursor.fetchone()

        if existing_location:
            return jsonify({'success': False, 'message': 'This location already exists', 'location_id': existing_location[0]}), 400
        # Insert new location
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
def fetch_and_save_weather():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    location_id = data.get('location_id')

    if not all([latitude, longitude, location_id]):
        return jsonify({'success': False, 'message': 'Latitude, longitude, and location_id are required'}), 400

    try:
        # Your existing code to fetch data from the API
        start = arrow.now().to('UTC')
        end = arrow.now().shift(days=5).to('UTC')
        
        params = {
            'lat': latitude,
            'lng': longitude,
            'start': start.timestamp(),
            'end': end.timestamp(),
        }
        
      

        # Fetch sea level and weather data
        sea_level_data = fetch_data('tide/sea-level', params)
        weather_data = fetch_data('weather', params,  extra_params={
            'params': 'windSpeed,windDirection,swellDirection,swellPeriod,swellHeight,waveHeight,wavePeriod,waterTemperature,airTemperature'
        })

        # Prepare lists to hold data
        sea_level_records = []
        weather_records = []

        # Process sea level data
        for sea_level in sea_level_data.get('data', []):
            record = {
                'time': arrow.get(sea_level['time']).to('UTC').format('YYYY-MM-DD HH:00'),
                'sea-level': sea_level.get('sg', 'N/A')
            }
            sea_level_records.append(record)

        # Process weather data
        for weather in weather_data.get('hours', []):
            record = {
                'time': arrow.get(weather['time']).to('UTC').format('YYYY-MM-DD HH:00'),
                'swellDirection': weather.get('swellDirection', {}).get('sg', 'N/A'),
                'swellHeight': weather.get('swellHeight', {}).get('sg', 'N/A'),
                'swellPeriod': weather.get('swellPeriod', {}).get('sg', 'N/A'),
                'waveHeight': weather.get('waveHeight', {}).get('sg', 'N/A'),
                'wavePeriod': weather.get('wavePeriod', {}).get('sg', 'N/A'),
                'windDirection': weather.get('windDirection', {}).get('sg', 'N/A'),
                'windSpeed': weather.get('windSpeed', {}).get('sg', 'N/A'),
                'waterTemperature': weather.get('waterTemperature', {}).get('sg', 'N/A'),
                'airTemperature': weather.get('airTemperature', {}).get('sg', 'N/A')
            }
            weather_records.append(record)

        # Convert lists to DataFrames
        df_sea_level = pd.DataFrame(sea_level_records)
        df_weather = pd.DataFrame(weather_records)

        # Create a complete time range starting from midnight
        date_range = pd.date_range(start=start.format('YYYY-MM-DD') + ' 00:00', end=end.format('YYYY-MM-DD') + ' 23:00', freq='H')
        df_complete = pd.DataFrame(date_range, columns=['time'])

        # Convert 'time' columns to datetime64[ns]
        df_complete['time'] = pd.to_datetime(df_complete['time'])
        df_sea_level['time'] = pd.to_datetime(df_sea_level['time'])
        df_weather['time'] = pd.to_datetime(df_weather['time'])

        # Merge DataFrames on 'time'
        df_sea_level = df_complete.merge(df_sea_level, on='time', how='left')
        df_weather = df_complete.merge(df_weather, on='time', how='left')

        # Combine DataFrames
        df_combined = pd.merge(df_sea_level, df_weather, on='time', how='left')

        # Add constant columns
        df_combined['longitude'] = params['lng']
        df_combined['latitude'] = params['lat']
        df_combined['date-of-api-call'] = start.format('YYYY-MM-DD')



        df_combined = df_combined.dropna()
        # Reorder columns to move longitude, latitude, and date-of-api-call to the front
        columns_order = ['longitude', 'latitude', 'date-of-api-call'] + [col for col in df_combined.columns if col not in ['longitude', 'latitude', 'date-of-api-call']]
        df_combined = df_combined[columns_order]

        # Prepare data for database insertion
        df_combined['location_id'] = location_id
        df_combined['forecast_date'] = pd.to_datetime(df_combined['time']).dt.date
        df_combined['time'] = pd.to_datetime(df_combined['time']).dt.time

        # Rename columns to match database schema
        column_mapping = {
            'sea-level': 'sea_level',
            'swellDirection': 'swell_direction',
            'swellHeight': 'swell_height',
            'swellPeriod': 'swell_period',
            'waveHeight': 'wave_height',
            'wavePeriod': 'wave_period',
            'windDirection': 'wind_direction',
            'windSpeed': 'wind_speed',
            'waterTemperature': 'water_temperature',
            'airTemperature': 'air_temperature'
        }
        df_combined.rename(columns=column_mapping, inplace=True)

        # Get the database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query for inserting data into weatherdata
        insert_query = """
        INSERT INTO weatherdata 
        (location_id, forecast_date, time, sea_level, swell_direction, swell_height, swell_period, 
         wave_height, wave_period, wind_direction, wind_speed, water_temperature, air_temperature)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Iterate over the dataframe rows and insert data into MySQL
        for index, row in df_combined.iterrows():
            cursor.execute(insert_query, (
                row['location_id'], 
                row['forecast_date'], 
                row['time'], 
                row['sea_level'], 
                row['swell_direction'], 
                row['swell_height'], 
                row['swell_period'], 
                row['wave_height'], 
                row['wave_period'], 
                row['wind_direction'], 
                row['wind_speed'], 
                row['water_temperature'], 
                row['air_temperature']
            ))

        # Commit the transaction
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Weather data fetched and saved successfully'})

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'message': f'API request failed: {str(e)}'}), 500
    except Error as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}), 500

# Helper function to fetch data from API
def fetch_data(endpoint, params, extra_params=None):
    url = f'https://api.stormglass.io/v2/{endpoint}/point'
    all_params = {**params, **(extra_params or {})}
    
    # Try using the primary API key first
    api_key = Config.SECRET_KEY1
    response = requests.get(url, params=all_params, headers={'Authorization': api_key})

    # Check if the response indicates the primary key is exhausted
    if response.status_code == 429:  # Rate limit exceeded
        print("Primary API key exhausted, switching to secondary key.")
        # Switch to the secondary API key
        api_key = Config.SECRET_KEY2
        response = requests.get(url, params=all_params, headers={'Authorization': api_key})

    # Raise an error if the response is still not successful
    response.raise_for_status()
    
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
