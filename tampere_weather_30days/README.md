# Tampere Weather Visualization - Latest 30 Days

This project creates a 3D visualization of Tampere weather conditions for the latest 30 days.

## Features

- **3D Pillars**: Show daily minimum and maximum temperatures as vertical pillars
- **Typical Temperature Lines**: Display typical maximum and minimum temperature ranges with dots and lines
- **Interactive Visualization**: 3D matplotlib plot that can be rotated and zoomed
- **Data Summary**: Prints weather statistics including coldest/hottest days

## Data Visualization Elements

1. **Blue Pillars**: Represent the temperature range from daily minimum to daily maximum
2. **Red Dashed Line with Dots**: Typical maximum temperature (high)
3. **Orange Dashed Line with Dots**: Typical maximum temperature (low)
4. **Light Blue Dotted Line with Dots**: Typical minimum temperature (high)
5. **Dark Blue Dotted Line with Dots**: Typical minimum temperature (low)

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy
- openpyxl (for Excel file reading)

## Usage

1. Ensure `Tampere.xlsx` is in the parent directory
2. Run the visualization:
   ```bash
   python main.py
   ```

## Data Source

The visualization reads weather data from `Tampere.xlsx` which should contain columns:
- DateTime
- Minimum temperature
- Maximum temperature
- Typical maximum temperature (high)
- Typical maximum temperature (low)
- Typical minimum temperature (high)
- Typical minimum temperature (low)

## Output

- Interactive 3D plot showing temperature patterns
- Console output with weather statistics and data summary