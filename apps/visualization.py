import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import matplotlib.pyplot as plt

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    @st.cache(persist= True)
    def load_data(region):
        if region == 'Chicago':
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/chicago-subset-cleaned.csv")
        else:
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Maharashtra_Synthetic_dataset.csv")
        return df

    def categories_func(region):
        Number_crimes = df['Primary Type'].value_counts()[:15]
        values = Number_crimes.values
        categories = pd.DataFrame(data= Number_crimes.index, columns=["Primary Type"])
        categories['values'] = values
        if region == 'Chicago':
            treemap(categories, 'Major 15 Crimes in Chicago', ['Primary Type'], categories['values'])
        else:
            treemap(categories, 'Major 15 Crimes in Maharashtra', ['Primary Type'], categories['values'])

    def treemap(categories, title, path, values):
        fig = px.treemap(categories, path= path, values= values, height= 700, title= title, color_discrete_sequence= px.colors.sequential.RdBu)
        fig.data[0].textinfo = 'label+text+value'
        st.write(fig)

    # Pie chart for Years of Crime
    def years_pie(region):
        if region == 'Chicago':
            st.subheader("Crime throughout the Years in Chicago")
        else:
            st.subheader("Crime throughout the Years in Maharashtra")
        Number_crimes_year = df['Year'].value_counts()
        years = pd.DataFrame(data= Number_crimes_year.index, columns=["Year"])
        years['values'] = Number_crimes_year.values
        fig = px.pie(years, values='values', names='Year', color_discrete_sequence=px.colors.sequential.Plasma, hover_data=['values'], labels={'values':'Crime'})
        fig.update_layout(margin= dict(t= 0, b= 0, l= 0, r= 0)) # To increase the shape of pie plot to fit the page layout
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.write(fig)

    # Arrest diagram
    def arrests():
        select_arrest = st.selectbox("Arrested?", [True, False])
        # Grouping dataset by year and arrests
        arrest_per_year = df.groupby('Year')['Arrest'].value_counts().rename('Counts').to_frame()
        arrest_per_year['Percentage'] = (100 * arrest_per_year / arrest_per_year.groupby(level=0).sum())
        arrest_per_year.reset_index(level=[1],inplace=True)

        line_plot = arrest_per_year[arrest_per_year['Arrest'] == select_arrest]['Percentage']
        fig= plt.figure(figsize=(12, 10))
        if select_arrest == True:
            plt.title('Percentages of successful arrests')
            plt.xlabel("Year")
            plt.ylabel("Successful Arrest Percentage")
        elif select_arrest == False:
            plt.title('Percentages of unsuccessful arrests')
            plt.xlabel("Year")
            plt.ylabel("Unsuccessful Arrest Percentage")
        plt.xticks(line_plot.index, line_plot.index.values)
        line_plot.plot(grid=True, marker='o', color='mediumvioletred')
        st.pyplot(fig)

    # Main Panel
    region = st.sidebar.radio("Select the region", ('Maharashtra', 'Chicago'))
    df = load_data(region)
    categories_func(region)
    years_pie(region)
    arrests()