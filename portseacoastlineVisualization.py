import folium
import math

# Coordinates for the location
latitude = -38.3340
longitude = 144.7019

# Dummy data
wind_speed = 5.2  # in m/s
wind_direction = 270  # in degrees (west)
swell_direction = 180  # in degrees (south)
wave_period = 10  # in seconds

# Function to calculate the end coordinates for the arrow/line
def calculate_end_coords(lat, lon, direction, distance):
    R = 6371e3  # Earth radius in meters
    brng = math.radians(direction)  # Convert bearing to radians

    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                     math.cos(lat1) * math.sin(distance / R) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(distance / R) * math.cos(lat1),
                             math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2, lon2

# Create a map centered around the location
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Calculate end coordinates for wind direction arrow
wind_end_lat, wind_end_lon = calculate_end_coords(latitude, longitude, wind_direction, wind_speed * 1000)

# Add wind direction arrow
folium.PolyLine(
    locations=[(latitude, longitude), (wind_end_lat, wind_end_lon)],
    color='blue',
    weight=2,
    opacity=1
).add_to(m)

# Calculate end coordinates for swell direction line
swell_end_lat, swell_end_lon = calculate_end_coords(latitude, longitude, swell_direction, 1000)

# Add swell direction line
folium.PolyLine(
    locations=[(latitude, longitude), (swell_end_lat, swell_end_lon)],
    color='red',
    weight=2,
    opacity=1,
    dash_array='5, 5'  # Dashed line
).add_to(m)

# Save map to HTML
m.save('stylized_surf_quality_map.html')

# Output a message to let the user know the map has been created
print('Stylized map has been created and saved to stylized_surf_quality_map.html')
