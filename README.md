# Synthetic AQI Dashboard

This is a Streamlit web application that generates and visualizes synthetic Air Quality Index (AQI) data for multiple cities. Users can customize parameters, view various interactive charts, and download the generated data as CSV.

## Features

- Generate synthetic hourly AQI data for multiple locations
- Includes pollutants: PM2.5, PM10, CO, NO2, O3, SO2
- Daily and seasonal patterns plus outlier injection for realistic simulation
- Multiple visualization types: line, bar, area, scatter, box plots, and map
- Data export as CSV

## How to Run Locally

1. Clone this repository:
   ```bash
   git clone git@github.com:YOUR_USERNAME/synthetic-aqi-dashboard.git
   cd synthetic-aqi-dashboard

2. (Optional) Create a virtual environment:

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install dependencies:
    pip install -r requirements.txt

    Run the app:
    streamlit run app.py
