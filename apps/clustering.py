import streamlit as st 
import pandas as pd 
import numpy as np 
import folium
import random
from streamlit_folium import folium_static
from geopy.distance import great_circle
from sklearn.cluster import DBSCAN

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")

    # Sidebar
    st.sidebar.markdown("Choose the Year for data to be displayed")
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(2003, 2022))))
    hour = st.sidebar.slider("Hour to look", 0, 24)

    @st.cache(persist= True)
    def load_data(selected_year):
        df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/" + str(selected_year) + ".csv")
        df['Date/Time of Crime'] = pd.to_datetime(df['Date/Time of Crime'], format= '%Y-%m-%d %H:%M:%S')
        return df

    def dbscan_cluster(selected_year, hour):
        df = load_data(selected_year)
        data1 = df[df['Date/Time of Crime'].dt.hour == hour]
        # Metric custom function for DBSCAN
        def greatcircle(x, y):
            lat1, long1 = x[0], x[1]
            lat2, long2 = y[0], y[1]
            dist = great_circle((lat1,long1),(lat2,long2)).meters
            return dist
        # Clustering based on Latitude and Longitude
        df_dbs = data1
        lat_long = df_dbs[['Latitude', 'Longitude']]
        # Converting into Numpy array
        X = lat_long.values 
        dbs = DBSCAN(eps= 500, min_samples= 10, metric= greatcircle, n_jobs= -1).fit(X) # eps=500 distance in meters
        labels = dbs.labels_
        df_dbs['Clusters'] = labels
        # Setting random color
        col_lst = []
        for i in range(0, df_dbs.Clusters.nunique()+1):
            r = "#%06x" % random.randint(0, 0xFFFFFF)
            col_lst.append(r)
        # Mapping
        location = df_dbs['Latitude'].mean(), df_dbs['Longitude'].mean()
        m = folium.Map(location= location, zoom_start= 10)
        folium.TileLayer('cartodbpositron').add_to(m)
        clust_colours = col_lst
        for i in range(0,len(df_dbs)):
            colouridx = df_dbs['Clusters'].iloc[i]
            if colouridx == -1:
                pass
            else:
                col = clust_colours[colouridx%len(clust_colours)]
                folium.CircleMarker(
                    [df_dbs['Latitude'].iloc[i], df_dbs['Longitude'].iloc[i]], 
                    radius = 10, 
                    color = col, 
                    fill = col).add_to(m)
        folium_static(m)
    
    # Main
    dbscan_cluster(selected_year, hour)