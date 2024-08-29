from flask import Flask, render_template, request, jsonify
import os
import mysql.connector
from utils import calculate_distance, get_hemisphere, closest_point
from database import query_all_users

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
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

if __name__ == '__main__':
    app.run(debug=True)
