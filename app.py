from flask import Flask, render_template, request, jsonify
import json
from math import sin, cos, sqrt, atan2, radians
import os

app = Flask(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula to calculate the distance
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

def get_hemisphere(lat, lon):
    if lat >= 0 and lon >= 0:
        return "NE"  # Northern Hemisphere and Eastern Hemisphere
    elif lat >= 0 and lon < 0:
        return "NW"  # Northern Hemisphere and Western Hemisphere
    elif lat < 0 and lon >= 0:
        return "SE"  # Southern Hemisphere and Eastern Hemisphere
    else:
        return "SW"  # Southern Hemisphere and Western Hemisphere

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/closest_point', methods=['GET'])
def closest_point():
    try:
        lng = float(request.args.get('lng'))
        lat = float(request.args.get('lat'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid latitude or longitude'}), 400

    # Determine which hemisphere file to load
    user_hemisphere = get_hemisphere(lat, lng)
    hemisphere_file = f'static/coastlines_{user_hemisphere}.json'
    
    try:
        with open(hemisphere_file) as f:
            coastlines_data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Coastline data file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding coastline data'}), 500

    # Define the search radius in kilometers (e.g., 100 km)
    search_radius = 100
    closest_point = None
    min_distance = float('inf')

    # Loop through each feature and calculate the closest point in the same hemisphere within the search radius
    for feature in coastlines_data['features']:
        if feature['geometry']['type'] == 'LineString':
            for coord in feature['geometry']['coordinates']:
                coord_lng, coord_lat = coord
                distance = calculate_distance(lat, lng, coord_lat, coord_lng)
                if distance <= search_radius and distance < min_distance:
                    min_distance = distance
                    closest_point = coord

    if closest_point:
        return jsonify({
            'lat': closest_point[1],
            'lng': closest_point[0]
        })
    else:
        return jsonify({'error': f'No coastline data available within {search_radius} km'}), 404

if __name__ == '__main__':
    app.run(debug=True)
