mapboxgl.accessToken = 'pk.eyJ1Ijoic2FtZHAiLCJhIjoiY20wYzJ5ZGh4MGZxbDJzb2Y1bmo4cjY0bSJ9.videznhMMGWJuY9_6QKMpA';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v11',
    center: [0, 0],
    zoom: 2
});

var marker = new mapboxgl.Marker();
var coastlineLayerVisible = false;
var closestCoastline = null;

map.on('load', function () {
    map.addSource('coastlines', {
        'type': 'geojson',
        'data': '/static/json/interpolated_coastlines.json'
    });

    map.addLayer({
        'id': 'coastlines-layer',
        'type': 'line',
        'source': 'coastlines',
        'layout': {},
        'paint': {
            'line-color': '#ff0000',
            'line-width': 2
        }
    });

    map.setLayoutProperty('coastlines-layer', 'visibility', 'none');
});

document.getElementById('toggle-coastline').addEventListener('change', function() {
    coastlineLayerVisible = !coastlineLayerVisible;
    map.setLayoutProperty('coastlines-layer', 'visibility', coastlineLayerVisible ? 'visible' : 'none');
});

map.on('click', function(e) {
    const lng = e.lngLat.lng.toFixed(5);
    const lat = e.lngLat.lat.toFixed(5);

    document.getElementById('coords').textContent = `Clicked Latitude: ${lat}, Longitude: ${lng}`;

    fetch(`/closest_point?lng=${lng}&lat=${lat}`)
        .then(response => response.json())
        .then(data => {
            if (data.lat && data.lng) {
                document.getElementById('coords').textContent +=
                    ` | Closest Coastline Latitude: ${data.lat.toFixed(5)}, Longitude: ${data.lng.toFixed(5)}`;

                closestCoastline = { lat: data.lat.toFixed(5), lng: data.lng.toFixed(5) };

                marker.setLngLat([data.lng, data.lat])
                    .setPopup(new mapboxgl.Popup({ offset: 25 }).setText(`Closest Coastline Latitude: ${data.lat.toFixed(5)}, Longitude: ${data.lng.toFixed(5)}`))
                    .addTo(map)
                    .togglePopup();
            } else {
                document.getElementById('coords').textContent += ' | Not close enough to a coastline';
                closestCoastline = null;
            }
        })
        .catch(error => {
            document.getElementById('coords').textContent += ' | Error fetching closest coastline data';
            console.error(error);
            closestCoastline = null;
        });
});

document.getElementById('get-surf-report').addEventListener('click', function() {
    if (closestCoastline) {
        document.getElementById('coastline-info').style.display = 'block';
        document.getElementById('coastline-coords').textContent =
            `Latitude: ${closestCoastline.lat}, Longitude: ${closestCoastline.lng}`;
    } else {
        alert('No coastline data available. Please click on the map first.');
    }
});

document.getElementById('close-coastline-info').addEventListener('click', function() {
    document.getElementById('coastline-info').style.display = 'none';
});

document.getElementById('get-surf-report').addEventListener('click', function() {
    if (closestCoastline) {
        document.getElementById('coastline-info').style.display = 'block';
        document.getElementById('coastline-coords').textContent =
            `Latitude: ${closestCoastline.lat}, Longitude: ${closestCoastline.lng}`;

        let locationName = prompt("Enter a name for this location:", "Unnamed Location");
        if (locationName === null) {
            return;
        }

        fetch('/save_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                latitude: closestCoastline.lat,
                longitude: closestCoastline.lng,
                name: locationName
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                return fetch('/fetch_and_save_weather', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ longitude: closestCoastline.lng, latitude: closestCoastline.lat }),
                });
            } else {
                console.error('Error saving location:', data.error);
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Weather and forecast data:", data);
            // Further process data or display charts, etc.
        })
        .catch((error) => {
            console.error('Error fetching weather:', error);
        });
    }
});
