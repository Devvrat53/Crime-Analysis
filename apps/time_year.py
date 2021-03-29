from altair.vegalite.v4.schema.channels import Latitude, Longitude
import streamlit as st
import numpy as np
import pandas as pd 
import random
import json
import plotly.express as px
import pydeck as pdk
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from geopy.distance import great_circle
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    st.sidebar.markdown("Choose the Year for data to be displayed")
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(2003, 2022))))
    hour = st.sidebar.slider("Hour to look", 0, 24)
    
    @st.cache(persist= True)
    def load_data(selected_year):
        df = pd.read_csv("/Users/devvratmungekar/Downloads/Year_Wise_Data/" + str(selected_year) + ".csv")
        df['Date/Time of Crime'] = pd.to_datetime(df['Date/Time of Crime'], format= '%Y-%m-%d %H:%M:%S')
        return df

    # PyDeck Plot
    def pydeck_plot(selected_year, hour):
        df = load_data(selected_year)
        data = df[df['Date/Time of Crime'].dt.hour == hour]
        st.markdown("Time of the day in which crime occurs")
        st.write(data.head(10))

        st.markdown("Crime between %i:00 and %i:00" % (hour, (hour+1) % 24))
        midpoint = (np.average(data['Latitude']), np.average(data['Longitude']))

        st.pydeck_chart(pdk.Deck(
            map_style= "mapbox://styles/mapbox/light-v9", 
            initial_view_state= {
                'latitude': midpoint[0],
                'longitude': midpoint[1],
                'zoom': 10.5,
                'pitch': 50,
            },
            layers= [
                pdk.Layer(
                    "HexagonLayer",
                    data= data[['Date/Time of Crime', 'Latitude', 'Longitude']],
                    get_position= ['Longitude', 'Latitude'],
                    radius= 100, # radius of the individual points
                    extruded= True, # Converts a 2D representation to 3D
                    auto_highlight= True,
                    pickable= True,
                    elevation_scale= 4,
                    elevation_range= [0, 1000]
                ),
            ],
        ))
    
    # Main - App
    pydeck_plot(selected_year, hour)

    '''st.subheader("Breakdown by the type of Crime")
    crime_select = st.selectbox("Select the type off Crime", list(df['Primary Type'].unique()))
    df_crime = df[df['Primary Type'] == crime_select]
    st.write(df_crime.head(10))
    st.write(df_crime.shape)
    midpoint_crime = (np.average(df_crime['Latitude']), np.average(df_crime['Longitude']))

    st.pydeck_chart(pdk.Deck(
        map_style= "mapbox://styles/mapbox/light-v9", 
        initial_view_state= {
            'latitude': midpoint[0],
            'longitude': midpoint[1],
            'zoom': 10.5,
            'pitch': 50,
        },
        layers= [
            pdk.Layer(
                "ScatterplotLayer",
                data= df_crime[['Primary Type', 'Latitude', 'Longitude']],
                get_position= ['Longitude', 'Latitude'],
                radius= 1000, # radius of the individual points
                auto_highlight= True,
                pickable= True,
                radius_scale=6,
                radius_min_pixels=1,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_fill_color=[255, 140, 0],
                get_line_color=[0, 0, 0],
            ),
        ],
    ))'''

    
