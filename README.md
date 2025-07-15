
# Time-Space Diagram Visualization Tool (for Ohio One Vehicle Data)

This repository contains a Python-based GUI tool for visualizing time-space diagrams using processed vehicle trajectory data from the Ohio One Vehicle Data.  It allows users to filter vehicles based on run number, sub run number, sub run start time, lane, time window, or spatial range, and generates interactive Plotly-based plots that visualize vehicle movement over time and space.

## Features
- Select run from available runs.
- Select sub run number from available runs.
- Select sub run start time from available runs.
- Filter vehicles by:
  - **Lane**
  - **Time window** or **Frenet X (space) range**
- Plot interactive **time-space diagrams** with Plotly showing:
  - Vehicle ID
  - Time
  - Frenet X
- Hoverable tooltips for detailed information on each data point.
- Output saved as an HTML file for easy sharing and viewing.

## Example Output
The tool generates an interactive HTML file (`Ohio_One_Vehicle_TS_Diagram.html`) containing the time-space diagram. The plot includes detailed hover information for each point and consistent color coding for vehicles, even if they have multiple trajectory segments.

## File Structure

├── ts_plotter.py        # Python script with GUI and plotting functions

└── README.md                    # This documentation file


## Dependencies
- `pandas`
- `plotly`
- `tkinter` (typically built-in with Python)

Install dependencies using:
bash
pip install pandas plotly


For systems where `tkinter` is not pre-installed (e.g., some Linux distributions), use:
bash
sudo apt-get install python3-tk


## How to Use
1. Place the main trajectory file (`Updated_Ohio_One_Vehicle.csv`) in the same directory as `ts_plotter.py`.
2. Run the Python script:
\`\`\`bash
python time_space_plotter.py
\`\`\`
3. A GUI window will appear with the following steps:

   - Select a **run number**, **sub run number**, and **sub run start time**.
   - Select a **Lane**.
   - Apply a filter:
     - **Time**: Set minimum and maximum time.
     - **Space**: Set minimum and maximum travelled distance.
   - Click **Update Vehicles** to populate the vehicle list based on the current filters.
   - Select one or more vehicles (or select all vehicles in the current run and lane).
   - Click **Plot Time-Space Diagram** to generate the interactive plot.
5. The interactive plot will:
   - Open automatically in your browser.
   - Save to `stationary_TS_Diagram.html` in the same folder.

## Notes
- Use the processed dataset with the added distance traveled column
- The vehicle list indicates ACC status by appending **(ACC)** next to the vehicle ID.

## License
This project is open-source and free to use for research and educational purposes.

## Author
**David Feng**  
Ph.D. Student, University of Virginia (UVA)  
Graduate Research Assistant, Turner-Fairbank Highway Research Center
"""
