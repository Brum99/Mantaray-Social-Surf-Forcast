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

    try:
        # Load coastline data from the static folder
        static_folder = app.static_folder
        with open(os.path.join(static_folder, 'interpolated_coastlines.json')) as f:
            coastlines_data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Coastline data file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding coastline data'}), 500

    closest_point = None
    min_distance = float('inf')

    # Loop through each feature and calculate the closest point
    for feature in coastlines_data['features']:
        if feature['geometry']['type'] == 'LineString':
            for coord in feature['geometry']['coordinates']:
                coord_lng, coord_lat = coord  # Ensure coordinates are accessed correctly
                distance = calculate_distance(lat, lng, coord_lat, coord_lng)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = coord

    if closest_point:
        return jsonify({
            'lat': closest_point[1],
            'lng': closest_point[0]
        })
    else:
        return jsonify({'error': 'No coastline data available'}), 404

if __name__ == '__main__':
    app.run(debug=True)
