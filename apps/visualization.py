import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import matplotlib.pyplot as plt

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    @st.cache(persist= True)
    def load_data():
        df = pd.read_csv("/Users/devvratmungekar/Downloads/chicago-subset-cleaned.csv")
        return df

    # Count Plot
    def plot_counts(feature_type, title, color):
        # Sidebar - Slider
        plot_df = pd.DataFrame(feature_type.value_counts()[:15])
        plot_df.columns = ["Freq"]
        plot_df["Type"] = plot_df.index
        fig = px.bar(plot_df, y="Freq", x="Type", text="Freq", color="Freq", color_continuous_scale= color)
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide", width= 900, height= 600)
        fig.update_layout(title_text= title)
        st.write(fig)

    # Pie chart for Years of Crime
    def years_pie():
        st.subheader("Crime throughout the Years")
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
            plt.title('Percentages of successful arrests from 2001 to 2021')
            plt.xlabel("Year")
            plt.ylabel("Successful Arrest Percentage")
        elif select_arrest == False:
            plt.title('Percentages of unsuccessful arrests from 2001 to 2021')
            plt.xlabel("Year")
            plt.ylabel("Unsuccessful Arrest Percentage")
        plt.xticks(line_plot.index, line_plot.index.values)
        line_plot.plot(grid=True, marker='o', color='mediumvioletred')
        st.pyplot(fig)

    # Main Panel
    df = load_data()
    plot_counts(df["Primary Type"], "Top 15 Crimes", 'Plasma')
    plot_counts(df['Location Description'], "Top 15 Crime Locations", 'Viridis')
    years_pie()
    arrests()