import streamlit as st 
import base64
import pandas as pd
import folium
from streamlit_folium import folium_static

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    #st.subheader("This is the web-application for analysing the data from the police record and provide meaning prediction from the same.")

    region = st.sidebar.radio("Select the region", ('Chicago', 'Maharashtra'))
    if region == 'Chicago':
    # GIF from Local system
        file_ = open("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/1989_2019_permits.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src= "data:image/gif;base64,{data_url}" alt= "cat.gif">', unsafe_allow_html= True)
    else:
        df_district = pd.read_excel("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/maharashtra_district.xlsx")
        m = folium.Map(location= [19.7515, 75.7139], zoom_start= 7)
        districts = folium.map.FeatureGroup()

        for name, lat, lng, in zip(df_district['place'],df_district['latitude'], df_district['longitude']):
            districts.add_child(
                folium.Marker(
                    [lat, lng],
                    popup= name,
                )
            )
        m.add_child(districts)

        folium_static(m)

