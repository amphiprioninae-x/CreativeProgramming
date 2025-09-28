"""
Tampere Weather Visualization - Latest 30 Days
3D pillar chart showing daily minimum and maximum temperatures
with typical temperature ranges displayed as dots and lines
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from datetime import datetime, timedelta
import os

class TampereWeatherVisualizer:
    def __init__(self, data_path):
        """Initialize with path to Excel data file"""
        self.data_path = data_path
        self.data = None
        
    def load_data(self):
        """Load weather data from Excel file"""
        try:
            # Try loading Excel file first, fallback to CSV if needed
            if os.path.exists(self.data_path.replace('.xlsx', '.csv')):
                self.data = pd.read_csv(self.data_path.replace('.xlsx', '.csv'), sep=';')
            else:
                self.data = pd.read_excel(self.data_path)
            
            # Convert DateTime column to datetime
            self.data['DateTime'] = pd.to_datetime(self.data['DateTime'])
            
            # Sort by date to ensure chronological order
            self.data = self.data.sort_values('DateTime')
            
            # Get the latest 30 days of data
            latest_date = self.data['DateTime'].max()
            thirty_days_ago = latest_date - timedelta(days=29)  # 29 + today = 30 days
            self.data = self.data[self.data['DateTime'] >= thirty_days_ago].copy()
            
            print(f"Loaded {len(self.data)} days of weather data")
            print(f"Date range: {self.data['DateTime'].min().strftime('%Y-%m-%d')} to {self.data['DateTime'].max().strftime('%Y-%m-%d')}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        
        return True
    
    def create_3d_visualization(self):
        """Create 3D visualization with transparent light blue cylinders and only typical max/min (high)"""
        if self.data is None:
            print("No data loaded. Please call load_data() first.")
            return

        # Prepare the figure
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Prepare data
        dates = self.data['DateTime']
        typical_max_high = self.data['Typical maximum temperature (high)']
        typical_min_low = self.data['Typical minimum temperature (low)']

        # Create x-axis positions (days)
        x_pos = np.arange(len(dates))

        # Draw transparent light blue cylinders for each day

        for i, (day, tmax, tmin) in enumerate(zip(x_pos, typical_max_high, typical_min_low)):
            # Cylinder parameters
            z = np.linspace(tmin, tmax, 30)
            theta = np.linspace(0, 2 * np.pi, 30)
            theta_grid, z_grid = np.meshgrid(theta, z)
            radius = 0.3
            x_grid = day + radius * np.cos(theta_grid)
            y_grid = radius * np.sin(theta_grid)
            ax.plot_surface(x_grid, y_grid, z_grid, color=(0.5, 0.8, 1, 0.4), alpha=0.4, linewidth=0, antialiased=True)

            # Draw dots at top and bottom with new colors
            ax.scatter([day], [0], [tmax], color='red', s=70, alpha=0.95)  # Top dot: red
            ax.scatter([day], [0], [tmin], color='yellow', s=70, alpha=0.95)  # Bottom dot: bright yellow

            # Link the two dots with an orange line
            ax.plot([day, day], [0, 0], [tmin, tmax], color='orange', linewidth=3, alpha=0.9)

        # Customize the plot
        ax.set_xlabel('Days (Latest 30 Days)', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Temperature (°C)', fontsize=12)
        ax.set_title('Tampere Weather Conditions - Latest 30 Days\n3D Cylinders: Typical Max/Min (High)', fontsize=14, fontweight='bold')

        # Set x-axis labels to show dates
        date_labels = [date.strftime('%m-%d') for date in dates]
        ax.set_xticks(x_pos[::3])  # Show every 3rd date to avoid crowding
        ax.set_xticklabels([date_labels[i] for i in range(0, len(date_labels), 3)], rotation=45)

        # Set y-axis to minimal range
        ax.set_ylim(-1, 1)
        ax.set_yticks([0])
        ax.set_yticklabels([''])

        # Adjust layout and show
        plt.tight_layout()
        plt.show()

def main():
    # Path to the Excel file (assuming it's in the parent directory)
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tampere.xlsx')
    
    # Create visualizer instance
    visualizer = TampereWeatherVisualizer(data_path)
    
    # Load data
    if visualizer.load_data():
        # Create and display the visualization
        visualizer.create_3d_visualization()
    else:
        print("Failed to load data. Please check the file path and format.")

if __name__ == "__main__":
    main()