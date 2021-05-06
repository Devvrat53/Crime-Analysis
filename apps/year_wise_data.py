import streamlit as st 
import pandas as pd 
import plotly.express as px
'''import seaborn as sns
import matplotlib.pyplot as plt 
st.set_option('deprecation.showPyplotGlobalUse', False)'''

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")

    @st.cache(persist= True)
    def load_data(selected_year, region):
        if region == 'Chicago':
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/" + str(selected_year) + ".csv")
        else:
            df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Maharashtra Year-wise Data/" + str(selected_year) + ".csv")
        return df

    def count_plot(feature_type, title, color):
        # Sidebar - Slider
        feature_type_nunique_count = feature_type.nunique()
        top_n_number = st.sidebar.slider(title, 1, feature_type_nunique_count, 15)
        plot_df = pd.DataFrame(feature_type.value_counts()[:top_n_number])
        plot_df.columns = ["Freq"]
        plot_df["Type"] = plot_df.index
        fig = px.bar(plot_df, y="Freq", x="Type", text="Freq", color="Freq", color_continuous_scale= color)
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide", width= 900, height= 600)
        fig.update_layout(title_text= title)
        st.write(fig)
        # Seaborn alternative code
        '''order_crime_location = df['Location Description'].value_counts().iloc[:15].index
        plt.figure(figsize= (15, 10))
        ax = sns.countplot(y= 'Location Description', data= df, order= order_crime_location)
        plt.title("Top 15 Crime Location")
        st.pyplot()'''

    # Main panel
    st.subheader("**Dataset**")
    region = st.sidebar.radio("Select the region", ('Maharashtra', 'Chicago'))
    st.sidebar.markdown("Choose the Year for data to be displayed")
    if region == 'Chicago':
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2001, 2022))))
        df = load_data(selected_year, region)
        st.write(df.head(10))
        count_plot(df['Primary Type'], "Top Crimes", 'Viridis')
        count_plot(df['Location Description'], "Top Crime Locations", 'Plasma')
    else:
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010, 2020))))
        df = load_data(selected_year, region)
        st.write(df.head(10))
        count_plot(df['Primary Type'], "Top Crimes", 'Viridis')
        count_plot(df['Location'], "Top Crime Locations", 'Plasma')


