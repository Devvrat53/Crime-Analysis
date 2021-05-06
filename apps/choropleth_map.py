import streamlit as st 
import pandas as pd 
import numpy as np
import json
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")

    region = st.sidebar.radio("Select the region", ('Maharashtra', 'Chicago'))
    if region == 'Chicago':
        st.sidebar.markdown("Choose the Year for data to be displayed")
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2003, 2022))))
    else:
        st.sidebar.markdown("Choose the Year for data to be displayed")
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010, 2020))))    
    

    @st.cache(persist= True, allow_output_mutation= True)
    def load_data(selected_year, region):
        if region == 'Chicago':
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/" + str(selected_year) + ".csv")
        else:
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Maharashtra Year-wise Data/" + str(selected_year) + ".csv")
        return df

    def choropleth_ward_year(selected_year, region):
        df = load_data(selected_year, region)
        df_Wards = df['Ward'].value_counts()
        result = pd.DataFrame(data= df_Wards.values, index=df_Wards.index, columns=['Count'])
        result = result.reindex(df.Ward.unique())
        result = result.reset_index()
        result.rename({'index': 'ward'}, inplace= True, axis= 1)
        result['ward'] = result['ward'].astype('str') # As 'ward' field in geojson file is a string

        st.subheader("Number of incidents per police ward")
        map1 = folium.Map(location= (41.895140898, -87.624255632), zoom_start= 10)
        if selected_year >= 2016:
            wards_geojson = json.load(open('/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/GeoJSON_files/Wards/Boundaries-Wards(2015-).geojson'))
        elif selected_year < 2016:
            wards_geojson = json.load(open('/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/GeoJSON_files/Wards/Boundaries-Wards(2003-2015).geojson'))

        choropleth1 = folium.Choropleth(
            geo_data= wards_geojson, 
            data= result, 
            columns= ['ward', 'Count'], 
            key_on= 'feature.properties.ward', 
            fill_color = 'YlOrRd', 
            fill_opacity = 0.7, 
            line_opacity = 0.2, 
            smooth_factor = 0,
            legend_name = 'Number of incidents per police ward'
        ).add_to(map1)

        # No information can be passed from the Folium on Browser interaction in Streamlit because folium_static doesn't support it.
        '''folium.LayerControl().add_to(map1)
        # Display Region Label
        choropleth1.geojson.add_child(
            folium.features.GeoJsonTooltip(['ward'], labels= False)'''

        folium_static(map1)

    def choropleth_district_year(selected_year, region):
        df = load_data(selected_year, region)

        df_District = df['District'].value_counts()
        result_District = pd.DataFrame(data= df_District.values, index=df_District.index, columns=['Count'])
        result_District = result_District.reindex(df.District.unique())
        result_District = result_District.reset_index()
        result_District.rename({'index': 'dist_num'}, inplace= True, axis= 1)
        result_District['dist_num'] = result_District['dist_num'].astype('str')

        st.subheader('Number of incidents per district')
        map2 = folium.Map(location= (41.895140898, -87.624255632), zoom_start= 10)
        district_geojson = json.load(open('/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/GeoJSON_files/Districts/Boundaries-Police_Districts_(current).geojson'))

        choropleth2 = folium.Choropleth(
            geo_data= district_geojson, 
            data= result_District, 
            columns= ['dist_num', 'Count'], 
            key_on= 'feature.properties.dist_num', 
            fill_color = 'YlOrRd', 
            fill_opacity = 0.7, 
            line_opacity = 0.2, 
            smooth_factor = 0,
            legend_name = 'Number of incidents per district'
        ).add_to(map2)

        '''folium.LayerControl().add_to(map1)
        # Display Region Label
        choropleth2.geojson.add_child(
            folium.features.GeoJsonTooltip(['dist_num'], labels= False)
        )'''

        folium_static(map2)

    def choropleth_community_year(selected_year, region):
        df = load_data(selected_year, region)

        df_community = df['Community Area'].value_counts()
        result_community = pd.DataFrame(data= df_community.values, index=df_community.index, columns=['Count'])
        result_community = result_community.reindex(df['Community Area'].unique())
        result_community = result_community.reset_index()
        result_community.rename({'index': 'area_num_1'}, inplace= True, axis= 1)
        result_community['area_num_1'] = result_community['area_num_1'].astype('str')
        result_community

        st.subheader('Number of incidents per community area')
        map3 = folium.Map(location= (41.895140898, -87.624255632), zoom_start= 10)
        community_geojson = json.load(open('/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/GeoJSON_files/Community_Areas/Boundaries-Community_Areas(current).geojson'))

        choropleth3 = folium.Choropleth(
            geo_data= community_geojson, 
            data= result_community, 
            columns= ['area_num_1', 'Count'], 
            key_on= 'feature.properties.area_num_1', 
            fill_color = 'YlOrRd', 
            fill_opacity = 0.7, 
            line_opacity = 0.2, 
            smooth_factor = 0,
            legend_name = 'Number of incidents per community area'
        ).add_to(map3)

        '''folium.LayerControl().add_to(map2)
        # Display Region Label
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['area_num_1'], labels= False)
        )'''

        folium_static(map3)

    if region == 'Chicago':
        ward_checkbox = st.sidebar.checkbox("Choropleth map of Ward")
        district_checkbox = st.sidebar.checkbox("Choropleth map of District")
        community_checkbox = st.sidebar.checkbox("Choropleth map of Community Area")

        if ward_checkbox:
            choropleth_ward_year(selected_year, region)
        if district_checkbox:
            choropleth_district_year(selected_year, region)
        if community_checkbox:
            choropleth_community_year(selected_year, region)
    else:
        maharashtra_checkbox = st.sidebar.checkbox("Choropleth map of the District")
        