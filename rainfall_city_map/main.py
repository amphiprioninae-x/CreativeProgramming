import requests
import matplotlib.pyplot as plt
import geopandas as gpd

# Placeholder for data fetching (replace URL with actual data source)
url = 'https://example.com/rainfall-data.csv'
response = requests.get(url)
# For demonstration, use mock data
cities = [
    {'name': 'CityA', 'lat': 34.05, 'lon': -118.25, 'rainfall': 500},
    {'name': 'CityB', 'lat': 40.71, 'lon': -74.00, 'rainfall': 800},
    {'name': 'CityC', 'lat': 51.51, 'lon': -0.13, 'rainfall': 600},
]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize=(10, 6))
world.plot(ax=ax, color='lightgray')

for city in cities:
    ax.scatter(city['lon'], city['lat'], s=city['rainfall']/2, alpha=0.7, label=city['name'])

ax.legend()
ax.set_title('Rainfall by City')
plt.show()
