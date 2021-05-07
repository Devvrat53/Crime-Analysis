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

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    @st.cache(persist= True)
    def load_data(selected_year, region):
        if region == 'Chicago':
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/" + str(selected_year) + ".csv")
        else:
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Maharashtra Year-wise Data/" + str(selected_year) + ".csv")
        df['Date/Time of Crime'] = pd.to_datetime(df['Date/Time of Crime'], format= '%Y-%m-%d %H:%M:%S')
        return df

    # PyDeck Plot
    def pydeck_plot(selected_year, region, hour):
        df = load_data(selected_year, region)
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

    # Main Panel
    region = st.sidebar.radio("Select the region", ('Chicago', 'Maharashtra'))
    if region == 'Chicago':
        st.sidebar.markdown("Choose the Year for data to be displayed")
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2003, 2022))))
        hour = st.sidebar.slider("Hour to look", 0, 24)
        pydeck_plot(selected_year, region, hour)
    else:
        st.sidebar.markdown("Choose the Year for data to be displayed")
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010, 2020))))
        hour = st.sidebar.slider("Hour to look", 0, 24)
        pydeck_plot(selected_year, region, hour)
    
