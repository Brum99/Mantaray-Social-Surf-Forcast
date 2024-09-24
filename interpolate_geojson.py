import json
import numpy as np
import os

def interpolate_line(coords, num_points=3):
    interpolated_coords = []
    for i in range(len(coords) - 1):
        start = np.array(coords[i])
        end = np.array(coords[i + 1])
        segment = np.linspace(start, end, num=num_points + 2)  # num_points + 2 to include both endpoints
        interpolated_coords.extend(segment.tolist())
    return interpolated_coords[:-1]  # Exclude the last point as it will be the start of the next segment

def process_geojson(input_file, output_file, num_points=3):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    for feature in data['features']:
        if feature['geometry']['type'] == 'LineString':
            original_coords = feature['geometry']['coordinates']
            feature['geometry']['coordinates'] = interpolate_line(original_coords, num_points)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

# Define file paths within the static folder
input_path = 'static/json/filtered_coastlines.json'
output_path = 'static/json/interpolated_coastlines.json'

# Process the GeoJSON file
process_geojson(input_path, output_path, num_points=3)
