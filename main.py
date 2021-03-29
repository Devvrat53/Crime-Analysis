import streamlit as st 
from multiapp import MultiApp
from apps import home, data, search_by, year_wise_data, time_year, choropleth_map, visualization, clustering
import pandas as pd 

app = MultiApp()
st.set_page_config(page_title= 'Welcome to Crime Analysis Application', layout= 'wide')

app.add_app("Home", home.app)
app.add_app("Data", data.app)
app.add_app("Visualization", visualization.app)
app.add_app("Search By", search_by.app)
app.add_app("Year-Wise-Data", year_wise_data.app)
app.add_app("Time", time_year.app)
app.add_app("Clustering", clustering.app)
app.add_app("Choropleth map", choropleth_map.app)
# Run the app
app.run()
