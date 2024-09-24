import json
from flask import jsonify
from math import sin, cos, sqrt, atan2, radians
import os

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

def closest_point(lng, lat, search_radius=100):
    # Determine which hemisphere file to load
    user_hemisphere = get_hemisphere(lat, lng)
    hemisphere_file = f'static/json/coastlines_{user_hemisphere}.json'
    
    # Print the path to debug
    print(f"Loading data from: {hemisphere_file}")

    try:
        with open(hemisphere_file) as f:
            coastlines_data = json.load(f)
    except FileNotFoundError:
        return {'error': 'Coastline data file not found'}, 500
    except json.JSONDecodeError:
        return {'error': 'Error decoding coastline data'}, 500

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

    # Print debug info
    if closest_point:
        print(f"Closest point found: {closest_point}")
        return {
            'lat': closest_point[1],
            'lng': closest_point[0]
        }, 200
    else:
        return {'error': f'No coastline data available within {search_radius} km'}, 404
