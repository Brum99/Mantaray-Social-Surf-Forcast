import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Provided wave height data
data = {'hours': [{'time': '2024-07-27T07:00:00+00:00', 'waveHeight': {'noaa': 0.67, 'sg': 0.67}},
                  {'time': '2024-07-27T08:00:00+00:00', 'waveHeight': {'noaa': 0.71, 'sg': 0.71}},
                  {'time': '2024-07-27T09:00:00+00:00', 'waveHeight': {'noaa': 0.76, 'sg': 0.76}},
                  {'time': '2024-07-27T10:00:00+00:00', 'waveHeight': {'noaa': 0.74, 'sg': 0.74}},
                  {'time': '2024-07-27T11:00:00+00:00', 'waveHeight': {'noaa': 0.73, 'sg': 0.73}},
                  {'time': '2024-07-27T12:00:00+00:00', 'waveHeight': {'noaa': 0.71, 'sg': 0.71}},
                  {'time': '2024-07-27T13:00:00+00:00', 'waveHeight': {'noaa': 0.75, 'sg': 0.75}},
                  {'time': '2024-07-27T14:00:00+00:00', 'waveHeight': {'noaa': 0.78, 'sg': 0.78}},
                  {'time': '2024-07-27T15:00:00+00:00', 'waveHeight': {'noaa': 0.82, 'sg': 0.82}},
                  {'time': '2024-07-27T16:00:00+00:00', 'waveHeight': {'noaa': 0.84, 'sg': 0.84}},
                  {'time': '2024-07-27T17:00:00+00:00', 'waveHeight': {'noaa': 0.85, 'sg': 0.85}},
                  {'time': '2024-07-27T18:00:00+00:00', 'waveHeight': {'noaa': 0.87, 'sg': 0.87}},
                  {'time': '2024-07-27T19:00:00+00:00', 'waveHeight': {'noaa': 1.01, 'sg': 1.01}},
                  {'time': '2024-07-27T20:00:00+00:00', 'waveHeight': {'noaa': 1.16, 'sg': 1.16}},
                  {'time': '2024-07-27T21:00:00+00:00', 'waveHeight': {'noaa': 1.3, 'sg': 1.3}},
                  {'time': '2024-07-27T22:00:00+00:00', 'waveHeight': {'noaa': 1.4, 'sg': 1.4}},
                  {'time': '2024-07-27T23:00:00+00:00', 'waveHeight': {'noaa': 1.51, 'sg': 1.51}},
                  {'time': '2024-07-28T00:00:00+00:00', 'waveHeight': {'noaa': 1.61, 'sg': 1.61}},
                  {'time': '2024-07-28T01:00:00+00:00', 'waveHeight': {'noaa': 1.6, 'sg': 1.6}},
                  {'time': '2024-07-28T02:00:00+00:00', 'waveHeight': {'noaa': 1.59, 'sg': 1.59}},
                  {'time': '2024-07-28T03:00:00+00:00', 'waveHeight': {'noaa': 1.58, 'sg': 1.58}},
                  {'time': '2024-07-28T04:00:00+00:00', 'waveHeight': {'noaa': 1.56, 'sg': 1.56}},
                  {'time': '2024-07-28T05:00:00+00:00', 'waveHeight': {'noaa': 1.54, 'sg': 1.54}},
                  {'time': '2024-07-28T06:00:00+00:00', 'waveHeight': {'noaa': 1.52, 'sg': 1.52}},
                  {'time': '2024-07-28T07:00:00+00:00', 'waveHeight': {'noaa': 1.47, 'sg': 1.47}},
                  {'time': '2024-07-28T08:00:00+00:00', 'waveHeight': {'noaa': 1.42, 'sg': 1.42}},
                  {'time': '2024-07-28T09:00:00+00:00', 'waveHeight': {'noaa': 1.37, 'sg': 1.37}},
                  {'time': '2024-07-28T10:00:00+00:00', 'waveHeight': {'noaa': 1.32, 'sg': 1.32}},
                  {'time': '2024-07-28T11:00:00+00:00', 'waveHeight': {'noaa': 1.26, 'sg': 1.26}},
                  {'time': '2024-07-28T12:00:00+00:00', 'waveHeight': {'noaa': 1.21, 'sg': 1.21}},
                  {'time': '2024-07-28T13:00:00+00:00', 'waveHeight': {'noaa': 1.15, 'sg': 1.15}},
                  {'time': '2024-07-28T14:00:00+00:00', 'waveHeight': {'noaa': 1.1, 'sg': 1.1}},
                  {'time': '2024-07-28T15:00:00+00:00', 'waveHeight': {'noaa': 1.04, 'sg': 1.04}},
                  {'time': '2024-07-28T16:00:00+00:00', 'waveHeight': {'noaa': 0.98, 'sg': 0.98}},
                  {'time': '2024-07-28T17:00:00+00:00', 'waveHeight': {'noaa': 0.92, 'sg': 0.92}},
                  {'time': '2024-07-28T18:00:00+00:00', 'waveHeight': {'noaa': 0.86, 'sg': 0.86}},
                  {'time': '2024-07-28T19:00:00+00:00', 'waveHeight': {'noaa': 0.81, 'sg': 0.81}},
                  {'time': '2024-07-28T20:00:00+00:00', 'waveHeight': {'noaa': 0.75, 'sg': 0.75}},
                  {'time': '2024-07-28T21:00:00+00:00', 'waveHeight': {'noaa': 0.7, 'sg': 0.7}},
                  {'time': '2024-07-28T22:00:00+00:00', 'waveHeight': {'noaa': 0.66, 'sg': 0.66}},
                  {'time': '2024-07-28T23:00:00+00:00', 'waveHeight': {'noaa': 0.63, 'sg': 0.63}},
                  {'time': '2024-07-29T00:00:00+00:00', 'waveHeight': {'noaa': 0.59, 'sg': 0.59}},
                  {'time': '2024-07-29T01:00:00+00:00', 'waveHeight': {'noaa': 0.56, 'sg': 0.56}},
                  {'time': '2024-07-29T02:00:00+00:00', 'waveHeight': {'noaa': 0.53, 'sg': 0.53}},
                  {'time': '2024-07-29T03:00:00+00:00', 'waveHeight': {'noaa': 0.5, 'sg': 0.5}},
                  {'time': '2024-07-29T04:00:00+00:00', 'waveHeight': {'noaa': 0.48, 'sg': 0.48}},
                  {'time': '2024-07-29T05:00:00+00:00', 'waveHeight': {'noaa': 0.46, 'sg': 0.46}},
                  {'time': '2024-07-29T06:00:00+00:00', 'waveHeight': {'noaa': 0.44, 'sg': 0.44}},
                  {'time': '2024-07-29T07:00:00+00:00', 'waveHeight': {'noaa': 0.43, 'sg': 0.43}},
                  {'time': '2024-07-29T08:00:00+00:00', 'waveHeight': {'noaa': 0.41, 'sg': 0.41}},
                  {'time': '2024-07-29T09:00:00+00:00', 'waveHeight': {'noaa': 0.4, 'sg': 0.4}}]}

# Parse the wave height data
times = [datetime.fromisoformat(hour['time']) for hour in data['hours']]
wave_heights = [hour['waveHeight']['noaa'] for hour in data['hours']]

# Create a DataFrame for easier plotting
df = pd.DataFrame({'Time': times, 'Wave Height (m)': wave_heights})

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['Wave Height (m)'], marker='o', linestyle='-', color='b')
plt.title('Wave Height Forecast')
plt.xlabel('Time')

plt.ylabel('Wave Height (m)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
