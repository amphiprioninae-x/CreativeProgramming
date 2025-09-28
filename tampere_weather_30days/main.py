"""
Tampere Weather Visualization - Latest 30 Days
3D pillar chart showing daily minimum and maximum temperatures
with typical temperature ranges displayed as dots and lines
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os
import mplcursors

class TampereWeatherVisualizer:
    def create_2d_pillar_visualization(self):
        """Create 2D vertical bar plot for daily min/max temperatures"""
        if self.data is None:
            print("No data loaded. Please call load_data() first.")
            return


        fig, ax = plt.subplots(figsize=(15, 7))
        dates = self.data['DateTime']
        min_temps = self.data['Minimum temperature']
        max_temps = self.data['Maximum temperature']
        precipitation = self.data['Precipitation']
        x_pos = np.arange(len(dates))

        # Draw precipitation as green bars on a secondary y-axis
        ax2 = ax.twinx()
        bar_width = 0.5
        bars = ax2.bar(x_pos, precipitation, width=bar_width, color='limegreen', alpha=0.5, label='Precipitation')
        ax2.set_ylabel('Precipitation (mm)', fontsize=12, color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # Add interactive tooltips for precipitation bars (no top-left display)
        cursor_precip = mplcursors.cursor(bars, hover=True)
        @cursor_precip.connect("add")
        def on_add_precip(sel):
            idx = sel.index
            value = precipitation.iloc[idx]
            sel.annotation.set_text(f"Precipitation: {value:.1f} mm")
            sel.annotation.get_bbox_patch().set(fc="limegreen", alpha=0.8)
            sel.annotation.get_bbox_patch().set_edgecolor("black")
        @cursor_precip.connect("remove")
        def on_remove_precip(sel):
            sel.annotation.set_visible(False)

        # Draw vertical blue bars for each day
        max_scatter = ax.scatter(x_pos, max_temps, color='red', s=70, alpha=0.95, label='Max Temp')
        min_scatter = ax.scatter(x_pos, min_temps, color='yellow', s=70, alpha=0.95, label='Min Temp')
        for i, (tmin, tmax) in enumerate(zip(min_temps, max_temps)):
            ax.vlines(x_pos[i], tmin, tmax, color='deepskyblue', alpha=0.6, linewidth=8, label='Min/Max Temp' if i == 0 else "")

        # Add interactive tooltips for the dots
        cursor = mplcursors.cursor([max_scatter, min_scatter], hover=True)
        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            if sel.artist == max_scatter:
                sel.annotation.set_text(f"Max Temp: {max_temps.iloc[idx]:.1f}°C")
                sel.annotation.get_bbox_patch().set(fc="red", alpha=0.8)
                sel.annotation.get_bbox_patch().set_edgecolor("black")
            else:
                sel.annotation.set_text(f"Min Temp: {min_temps.iloc[idx]:.1f}°C")
                sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.9)
                sel.annotation.get_bbox_patch().set_edgecolor("black")
        @cursor.connect("remove")
        def on_remove(sel):
            sel.annotation.set_visible(False)

        # Set x-axis labels to show dates
        date_labels = [date.strftime('%m-%d') for date in dates]
        ax.set_xticks(x_pos[::3])
        ax.set_xticklabels([date_labels[i] for i in range(0, len(date_labels), 3)], rotation=45)

        ax.set_xlabel('Days (Latest 30 Days)', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.set_title('Tampere Weather Conditions - Latest 30 Days\nDaily Min/Max Temperatures and Precipitation', fontsize=14, fontweight='bold')

        # Combine legends from both axes so 'Precipitation' appears in the main legend
        handles1, labels1 = ax.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        by_label = dict(zip(labels1 + labels2, handles1 + handles2))
        ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()
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
    
    def create_2d_visualization(self):
        """Create 2D visualization with vertical bars and colored dots/lines for typical max/min (high)"""
        if self.data is None:
            print("No data loaded. Please call load_data() first.")
            return

        # Prepare the figure
        fig, ax = plt.subplots(figsize=(15, 7))

        # Prepare data
        dates = self.data['DateTime']
        typical_max_high = self.data['Typical maximum temperature (high)']
        typical_min_low = self.data['Typical minimum temperature (low)']
        x_pos = np.arange(len(dates))

        # Draw vertical orange lines between min and max for each day
        for i, (tmax, tmin) in enumerate(zip(typical_max_high, typical_min_low)):
            ax.plot([x_pos[i], x_pos[i]], [tmin, tmax], color='orange', linewidth=4, alpha=0.8)
            ax.scatter(x_pos[i], tmax, color='red', s=80, zorder=3, label='Max (High)' if i == 0 else "")
            ax.scatter(x_pos[i], tmin, color='yellow', s=80, zorder=3, label='Min (Low)' if i == 0 else "")

        # Set x-axis labels to show dates
        date_labels = [date.strftime('%m-%d') for date in dates]
        ax.set_xticks(x_pos[::3])
        ax.set_xticklabels([date_labels[i] for i in range(0, len(date_labels), 3)], rotation=45)

        # Labels and title
        ax.set_xlabel('Days (Latest 30 Days)', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.set_title('Tampere Weather Conditions - Latest 30 Days\nMax (High) and Min (Low)', fontsize=14, fontweight='bold')

        # Add legend for ax only (no ax2 in this method)
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=11)

        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()

def main():
    # Path to the Excel file (assuming it's in the parent directory)
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tampere.xlsx')
    
    # Create visualizer instance
    visualizer = TampereWeatherVisualizer(data_path)
    
    # Load data
    if visualizer.load_data():
        # Create and display the 2D pillar visualization
        visualizer.create_2d_pillar_visualization()
    else:
        print("Failed to load data. Please check the file path and format.")

if __name__ == "__main__":
    main()