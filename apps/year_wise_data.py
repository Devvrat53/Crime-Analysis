import streamlit as st 
import pandas as pd 
import plotly.express as px
'''import seaborn as sns
import matplotlib.pyplot as plt 
st.set_option('deprecation.showPyplotGlobalUse', False)'''

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    
    # Sidebar - File Upload
    with st.sidebar.header("**File Upload**"):
        uploaded_file = st.sidebar.file_uploader("Upload your CSV data", type= ['csv'], accept_multiple_files= False)
        st.sidebar.markdown("[Example of CSV file](https://www.kaggle.com/currie32/crimes-in-chicago)")

    @st.cache(persist= True)
    def load_data(selected_year):
        df = pd.read_csv("/Users/devvratmungekar/Downloads/Year_Wise_Data/" + str(selected_year) + ".csv")
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
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown("Raw data")
        st.write(df.head(10))
        count_plot(df['Primary Type'], "Top Crimes", 'Viridis')
        count_plot(df['Location Description'], "Top Crime Locations", 'Viridis')
    else: 
        st.info("Awaiting for the CSV file to be uploaded! Here is the year-wise distribution of inbuilt dataset")
        st.markdown("Choose the Year for data to be displayed")
        selected_year = st.selectbox('Year', list(reversed(range(2001, 2022))))

        df = load_data(selected_year)
        st.write(df.head(10))
        count_plot(df['Primary Type'], "Top Crimes", 'Viridis')
        count_plot(df['Location Description'], "Top Crime Locations", 'Plasma')

