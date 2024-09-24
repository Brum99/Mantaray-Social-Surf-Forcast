import requests
import pandas as pd
import arrow
from config import Config
from database import get_db_connection

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

def fetch_and_save_weather_data(latitude, longitude, location_id):
    try:
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
        weather_data = fetch_data('weather', params, extra_params={
            'params': 'windSpeed,windDirection,swellDirection,swellPeriod,swellHeight,waveHeight,wavePeriod,waterTemperature,airTemperature'
        })

        # Process data and create DataFrame
        df_combined = process_weather_data(sea_level_data, weather_data, params, start)

        # Save data to database
        save_weather_data_to_db(df_combined, location_id)

        return {'success': True, 'message': 'Weather data fetched and saved successfully'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': f'API request failed: {str(e)}'}
    except Exception as e:
        return {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}

def process_weather_data(sea_level_data, weather_data, params, start):
    # Process sea level and weather data
    # Create and combine DataFrames
    # ... (implementation details)

    return df_combined

def save_weather_data_to_db(df_combined, location_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO weatherdata 
    (location_id, forecast_date, time, sea_level, swell_direction, swell_height, swell_period, 
     wave_height, wave_period, wind_direction, wind_speed, water_temperature, air_temperature)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for index, row in df_combined.iterrows():
        cursor.execute(insert_query, (
            location_id, 
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

    connection.commit()
    cursor.close()
    connection.close()