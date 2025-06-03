import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px 

############### GENERATE AQI DATA ################# 
# AQI breakpoints for calculation
breakpoints = {
    'PM2.5': [(0.0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
              (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300), (250.5, 350.4, 301, 400),
              (350.5, 500.4, 401, 500)],
    'PM10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200),
             (355, 424, 201, 300), (425, 504, 301, 400), (505, 604, 401, 500)],
    'CO': [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150),
           (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300), (30.5, 40.4, 301, 400),
           (40.5, 50.4, 401, 500)],
    'NO2': [(0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200),
            (650, 1249, 201, 300), (1250, 1649, 301, 400), (1650, 2049, 401, 500)],
    'O3': [(0.000, 0.054, 0, 50), (0.055, 0.070, 51, 100), (0.071, 0.085, 101, 150),
           (0.086, 0.105, 151, 200), (0.106, 0.200, 201, 300)],
    'SO2': [(0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150),
            (186, 304, 151, 200), (305, 604, 201, 300), (605, 804, 301, 400),
            (805, 1004, 401, 500)]
}

def calculate_aqi(conc, pollutant):
    bps = breakpoints.get(pollutant)
    if not bps:
        return None
    for (c_low, c_high, aqi_low, aqi_high) in bps:
        if c_low <= conc <= c_high:
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (conc - c_low) + aqi_low
            return round(aqi)
    return None

def add_daily_seasonal_pattern(base_value, hour, day_of_year, pollutant):
    daily_factor = 1
    if 7 <= hour <= 9 or 18 <= hour <= 21:
        daily_factor = 1.3
    elif 0 <= hour <= 5:
        daily_factor = 0.7
    else:
        daily_factor = 1.0

    if pollutant in ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO']:
        if day_of_year >= 335 or day_of_year <= 59:
            seasonal_factor = 1.4
        elif 150 <= day_of_year <= 250:
            seasonal_factor = 0.7
        else:
            seasonal_factor = 1.0
    else:
        seasonal_factor = 1.0

    return base_value * daily_factor * seasonal_factor

def generate_synthetic_aqi(num_hours):
    locations = [
        {'city': 'CityA', 'lat': 40.7128, 'lon': -74.0060},
        {'city': 'CityB', 'lat': 34.0522, 'lon': -118.2437},
        {'city': 'CityC', 'lat': 51.5074, 'lon': -0.1278},
        {'city': 'CityD', 'lat': 35.6895, 'lon': 139.6917},
        {'city': 'CityE', 'lat': 28.7041, 'lon': 77.1025},
    ]

    start_date = datetime.now()
    data = []

    for loc in locations:
        for i in range(num_hours):
            timestamp = start_date + timedelta(hours=i)
            hour = timestamp.hour
            day_of_year = timestamp.timetuple().tm_yday

            base_pm25 = np.random.uniform(5, 50)
            base_pm10 = np.random.uniform(10, 80)
            base_co = np.random.uniform(0.2, 8)
            base_no2 = np.random.uniform(10, 120)
            base_o3 = np.random.uniform(0.02, 0.09)
            base_so2 = np.random.uniform(5, 50)

            pm25 = add_daily_seasonal_pattern(base_pm25, hour, day_of_year, 'PM2.5')
            pm10 = add_daily_seasonal_pattern(base_pm10, hour, day_of_year, 'PM10')
            co = add_daily_seasonal_pattern(base_co, hour, day_of_year, 'CO')
            no2 = add_daily_seasonal_pattern(base_no2, hour, day_of_year, 'NO2')
            o3 = add_daily_seasonal_pattern(base_o3, hour, day_of_year, 'O3')
            so2 = add_daily_seasonal_pattern(base_so2, hour, day_of_year, 'SO2')

            # Inject outliers occasionally (~5%)
            if random.random() < 0.05:
                pm25 *= random.uniform(1.5, 3)
                pm10 *= random.uniform(1.5, 3)
                co *= random.uniform(1.5, 3)
                no2 *= random.uniform(1.5, 3)
                o3 *= random.uniform(1.5, 3)
                so2 *= random.uniform(1.5, 3)

            # Clip max values
            pm25 = min(pm25, 500)
            pm10 = min(pm10, 600)
            co = min(co, 50)
            no2 = min(no2, 2050)
            o3 = min(o3, 0.2)
            so2 = min(so2, 1005)

            aqi_pm25 = calculate_aqi(pm25, 'PM2.5')
            aqi_pm10 = calculate_aqi(pm10, 'PM10')
            aqi_co = calculate_aqi(co, 'CO')
            aqi_no2 = calculate_aqi(no2, 'NO2')
            aqi_o3 = calculate_aqi(o3, 'O3')
            aqi_so2 = calculate_aqi(so2, 'SO2')

            data.append({
                'timestamp': timestamp,
                'city': loc['city'],
                'latitude': loc['lat'],
                'longitude': loc['lon'],
                'PM2.5 (µg/m³)': round(pm25, 1),
                'PM10 (µg/m³)': round(pm10, 1),
                'CO (ppm)': round(co, 2),
                'NO2 (ppb)': round(no2, 1),
                'O3 (ppm)': round(o3, 3),
                'SO2 (ppb)': round(so2, 1),
                'AQI_PM2.5': aqi_pm25,
                'AQI_PM10': aqi_pm10,
                'AQI_CO': aqi_co,
                'AQI_NO2': aqi_no2,
                'AQI_O3': aqi_o3,
                'AQI_SO2': aqi_so2,
            })

    return pd.DataFrame(data)

# Streamlit UI
st.title("Synthetic AQI Data Generator & Visualizer")

hours = st.slider("Select number of hours to generate data:", 24, 168, 48, step=24)


if st.button("Generate Data"):
    with st.spinner("Generating synthetic AQI data..."):
        df = generate_synthetic_aqi(hours)
        st.session_state['df'] = df
    st.success("Data generated!")

if 'df' in st.session_state:
    df = st.session_state['df']
    st.dataframe(df)

    # CSV download
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='synthetic_aqi_data.csv',
        mime='text/csv'
    )

    # ------------------ Visualizations ------------------

    st.markdown("## Visualizations")

    # City selection (All or one)
    cities = ['All'] + list(df['city'].unique())
    selected_city = st.selectbox("Select city for visualization:", cities)

    if selected_city != 'All':
        viz_df = df[df['city'] == selected_city]
    else:
        viz_df = df.copy()

    pollutants = ['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'CO (ppm)', 'NO2 (ppb)', 'O3 (ppm)', 'SO2 (ppb)']
    selected_pollutant = st.selectbox("Select pollutant:", pollutants)

    # Line chart
    st.markdown("### Line Chart: Pollutant Over Time")
    fig_line = px.line(viz_df, x='timestamp', y=selected_pollutant,
                       color='city' if selected_city == 'All' else None,
                       title=f'{selected_pollutant} Over Time')
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar chart (only if all cities)
    if selected_city == 'All':
        st.markdown("### Bar Chart: Average Pollutant Level by City")
        avg_by_city = viz_df.groupby('city')[selected_pollutant].mean().reset_index()
        fig_bar = px.bar(avg_by_city, x='city', y=selected_pollutant,
                         title=f'Average {selected_pollutant} by City')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Area chart
    st.markdown("### Area Chart: Cumulative Pollutant Over Time")
    cum_df = viz_df.copy()
    cum_df['cumulative'] = cum_df[selected_pollutant].cumsum()
    fig_area = px.area(cum_df, x='timestamp', y='cumulative',
                      title=f'Cumulative {selected_pollutant} Over Time')
    st.plotly_chart(fig_area, use_container_width=True)

    # Scatter plot for two pollutants
    st.markdown("### Scatter Plot: Compare Two Pollutants")
    pollutant_x = st.selectbox("Select pollutant for X-axis:", pollutants, index=0, key='x')
    pollutant_y = st.selectbox("Select pollutant for Y-axis:", pollutants, index=1, key='y')
    fig_scatter = px.scatter(viz_df, x=pollutant_x, y=pollutant_y,
                             color='city' if selected_city == 'All' else None,
                             title=f'{pollutant_x} vs {pollutant_y}')
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Box plot
    st.markdown("### Box Plot: Pollutant Distribution")
    fig_box = px.box(viz_df, y=selected_pollutant,
                     x='city' if selected_city == 'All' else None,
                     title=f'{selected_pollutant} Distribution')
    st.plotly_chart(fig_box, use_container_width=True)

    # Map visualization
    st.markdown("### Map: Average AQI per City")

    def row_max_aqi(row):
        aqi_cols = ['AQI_PM2.5', 'AQI_PM10', 'AQI_CO', 'AQI_NO2', 'AQI_O3', 'AQI_SO2']
        return max([row[c] if row[c] is not None else 0 for c in aqi_cols])

    map_df = df.groupby(['city', 'latitude', 'longitude']).apply(
        lambda group: pd.Series({
            'avg_aqi': group.apply(row_max_aqi, axis=1).mean()
        })
    ).reset_index()

    fig_map = px.scatter_mapbox(
        map_df, lat='latitude', lon='longitude', size='avg_aqi',
        color='avg_aqi', color_continuous_scale=px.colors.sequential.Viridis,
        size_max=30, zoom=1,
        hover_name='city', hover_data={'latitude':False, 'longitude':False, 'avg_aqi':True},
        title='Average AQI by City'
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.info("Please generate data first.")