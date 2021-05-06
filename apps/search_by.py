import streamlit as st 
import pandas as pd

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    def load_data():
        df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/chicago-subset-cleaned.csv")
        return df

    def load_year_data():
        st.markdown("Choose the Year for data to be displayed")
        selected_year = st.selectbox('Year', list(reversed(range(2001, 2022))))
        df_year = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/" + str(selected_year) + ".csv")
        return df_year

    st.sidebar.markdown("Select the Field to be searched")
    select_box = st.sidebar.selectbox("", ['Case Number', 'Primary Type', 'Description', 'Location Description', 'Ward'])
    if select_box == 'Case Number':
        case_search = st.text_input("Enter the Case File No.")
        if case_search:
            df = load_data()
            case_search_query = df.query("`Case Number` == @case_search")
            st.write(case_search_query)
            st.write("The total returned data: ", case_search_query.shape)
    elif select_box == 'Primary Type':
        df_year = load_year_data()
        primary_select = st.selectbox("Select the type of Crime", list(df_year['Primary Type'].unique()))
        df_primary_type = df_year[df_year['Primary Type'] == primary_select]
        st.write(df_primary_type)
        st.write("The total returned data: ", df_primary_type.shape)
    elif select_box == 'Description':
        df_year = load_year_data()
        description_select = st.selectbox("Select the Description of Crime", list(df_year['Description'].unique()))
        df_description = df_year[df_year['Description'] == description_select]
        st.write(df_description)
        st.write("The total returned data: ", df_description.shape)
    elif select_box == 'Location Description':
        df_year = load_year_data()
        location_select = st.selectbox("Select the Location of Crime", list(df_year['Location Description'].unique()))
        df_location = df_year[df_year['Location Description'] == location_select]
        st.write(df_location)
        st.write("The total returned data: ", df_location.shape)
    elif select_box == 'Ward':
        ward_search = st.text_input("Enter the Ward No.")
        if ward_search:
            df = load_data()
            ward_search_query = df.query("`Ward` == @ward_search")
            st.write(ward_search_query)
            st.write("The total returned data: ", ward_search_query.shape)

