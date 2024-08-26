import requests
import datetime

import os 

API_KEY = os.getenv('STORMGLASS_API_KEY')

# Coordinates for the location
latitude = -38.3410
longitude = 144.7156

# Parameters you want to retrieve
params = 'waveHeight'

# Current UTC timestamp
start = datetime.datetime.utcnow().isoformat() + 'Z'

# API endpoint
url = 'https://api.stormglass.io/v2/weather/point'

# Headers for the request
headers = {
    'Authorization': API_KEY
}

# Query parameters for the request
query_params = {
    'lat': latitude,
    'lng': longitude,
    'params': params,
    'start': start
}

# Make the request
response = requests.get(url, headers=headers, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Print the wave height data
    print(data)
else:
    print(f'Error: {response.status_code}')
    print(response.json())
