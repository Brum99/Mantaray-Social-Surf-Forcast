import json

def split_coastline_data(coastline_data):
    NE, NW, SE, SW = [], [], [], []
    
    for feature in coastline_data['features']:
        if feature['geometry']['type'] == 'LineString':
            ne_coords = []
            nw_coords = []
            se_coords = []
            sw_coords = []
            
            for coord in feature['geometry']['coordinates']:
                lng, lat = coord
                if lat >= 0 and lng >= 0:
                    ne_coords.append(coord)
                elif lat >= 0 and lng < 0:
                    nw_coords.append(coord)
                elif lat < 0 and lng >= 0:
                    se_coords.append(coord)
                elif lat < 0 and lng < 0:
                    sw_coords.append(coord)
            
            if ne_coords:
                NE.append({
                    'type': 'Feature',
                    'properties': {
                        'featurecla': 'Coastline',
                        'scalerank': 0,
                        'min_zoom': 0.0
                    },
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': ne_coords
                    }
                })
            if nw_coords:
                NW.append({
                    'type': 'Feature',
                    'properties': {
                        'featurecla': 'Coastline',
                        'scalerank': 0,
                        'min_zoom': 0.0
                    },
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': nw_coords
                    }
                })
            if se_coords:
                SE.append({
                    'type': 'Feature',
                    'properties': {
                        'featurecla': 'Coastline',
                        'scalerank': 0,
                        'min_zoom': 0.0
                    },
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': se_coords
                    }
                })
            if sw_coords:
                SW.append({
                    'type': 'Feature',
                    'properties': {
                        'featurecla': 'Coastline',
                        'scalerank': 0,
                        'min_zoom': 0.0
                    },
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': sw_coords
                    }
                })

    return {'NE': NE, 'NW': NW, 'SE': SE, 'SW': SW}

# Load the original coastline data
with open('static/json/interpolated_coastlines.json') as f:
    coastline_data = json.load(f)

# Split the data
split_data = split_coastline_data(coastline_data)

# Save the split data to separate files
with open('static/json/coastlines_NE.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': split_data['NE']}, f)
with open('static/json/coastlines_NW.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': split_data['NW']}, f)
with open('static/json/coastlines_SE.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': split_data['SE']}, f)
with open('static/json/coastlines_SW.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': split_data['SW']}, f)
