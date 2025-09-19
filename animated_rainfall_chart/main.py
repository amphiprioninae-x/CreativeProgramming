import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from matplotlib.animation import FuncAnimation

# Mock data: 100 years, 12 months, 3 cities
years = 100
months = 12
cities = [
    {'name': 'CityA', 'lat': 34.05, 'lon': -118.25},
    {'name': 'CityB', 'lat': 40.71, 'lon': -74.00},
    {'name': 'CityC', 'lat': 51.51, 'lon': -0.13},
]
rainfall_data = np.random.rand(years, months, len(cities)) * 100

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize=(10, 6))
world.plot(ax=ax, color='lightgray')

scatters = [ax.scatter([], [], s=100, label=city['name']) for city in cities]
ax.legend()
ax.set_title('Animated Monthly Average Rainfall')

frames = years * months

def update(frame):
    year = frame // months
    month = frame % months
    ax.clear()
    world.plot(ax=ax, color='lightgray')
    for i, city in enumerate(cities):
        rainfall = rainfall_data[year, month, i]
        ax.scatter(city['lon'], city['lat'], s=rainfall, c='blue', alpha=0.7, label=city['name'])
    ax.legend()
    ax.set_title(f'Rainfall: Year {1925+year}, Month {month+1}')

ani = FuncAnimation(fig, update, frames=frames, interval=200)
plt.show()
