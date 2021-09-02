import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import matplotlib.pyplot as plt
from google.cloud import bigquery

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")

    def yearwise_data():
        df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/chicago-subset-cleaned.csv")
        df['Date/Time of Crime'] = pd.to_datetime(df['Date/Time of Crime'], format = '%Y-%m-%d %H:%M:%S')
        for i in range(2003, 2022):
            df_i = df[df['Year'] == i]
            df_i.to_csv('/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Year_Wise_Data/' + str(i) + '.csv')

    def Bigquery():
        ## create a service account, download the json file and export the credentials in the terminal
        project_id ='chicago-crimes-02092021'
        dataset_id = 'chicago-crimes-02092021:chicago_crimes'
        # Create a "Client" object
        client = bigquery.Client(project = project_id)
        # Construct a reference to the "chicago_crime" dataset
        dataset_ref = client.dataset(dataset_id)
        # API request - fetch the dataset
        #dataset = client.get_dataset(dataset_ref)
        # results to dataframe function
        def data_load(query):
            query = client.query(query)
            results = query.result()
            return results.to_dataframe() 

        query = f''' 
                    SELECT * FROM `chicago-crimes-02092021.chicago_crimes.cleaned_chicago_crimes` LIMIT 1000
                '''
        ## for query go to big query, then bigquery editor, then click on query table. After that copy the table name from the bigquery editor.

        """
        A useful function to estimate query size. 
        """

        def query_size(query, bq_client):
            # We initiate a `QueryJobConfig` object
            # API description: https://googleapis.dev/py/bigquery/latest/generated/google.cloud.bigquery.job.QueryJobConfig.html
            job_config = bigquery.QueryJobConfig()
            # We turn on 'dry run', by setting the `QueryJobConfig` object's `dry_run` attribute.
            # This means that we do not actually run the query, but estimate its running cost. 
            job_config.dry_run = True
            #When you repeat a query with the Use cached results option disabled, the existing cached result is overwritten.
            #This requires BigQuery to compute the query result, and you are charged for the query. 
            #This is particularly useful in benchmarking scenarios.
            job_config.use_query_cache = False

            # We activate the job_config by passing the `QueryJobConfig` to the client's `query` method.
            query_job = bq_client.query(query, job_config=job_config)

            # The results comes as bytes which we convert into Gigabytes for better readability
            return query_job.total_bytes_processed / 2**30

        def bigquery_app():
        # Main panel
            df = data_load(query)
            size = query_size(query, client)
            st.info(f'Query to gather data will process {size:.5f} GB on BigQuery.')
            st.write(df.head(20))
            '''data_cleaning()''' # Uncomment for Live Data Cleaning
            '''yearwise_data()''' # Uncomment to create year-wise data
        bigquery_app()

    def data_cleaning():
        df.drop(['ID','Block', 'IUCR', 'Domestic', 'Beat', 'FBI Code', 'X Coordinate', 'Y Coordinate', 'Year', 'Updated On', 'Location'], inplace= True, axis= 1)

        # Splitting date column into its individual components
        df['D'] = df['Date'].str.split('/').str[1]
        df['Month'] = df['Date'].str.split('/').str[0]
        df['Year'] = df['Date'].str.split('/').str[2]
        df['Y'] = df['Year'].str.split(' ').str[0]
        df['Time'] = df['Year'].str.split(' ').str[1]
        df['Am/Pm'] = df['Year'].str.split(' ').str[2]
        df['Time'] = df['Time'] + ' ' + df['Am/Pm']

        df.drop(['Year', 'Am/Pm'], inplace= True, axis= 1)

        df.rename(columns= {'Date': 'Date/Time of Crime'}, inplace= True)
        df.rename(columns= {'D': 'Date', 'Y': 'Year'}, inplace= True)
        # Dropping NULL values
        df.dropna(axis= 0, inplace= True)
        df[['Date', 'Month', 'Year', 'Ward', 'District', 'Community Area']] = df[['Date', 'Month', 'Year', 'Ward', 'District', 'Community Area']].astype('int64')
        # Converting 12 hours format into 24 hours format
        df['Time'] = pd.to_datetime(df['Time']).dt.time 
        df['Date/Time of Crime'] = pd.to_datetime(df['Date/Time of Crime'],format = '%m/%d/%Y %I:%M:%S %p')
        # Saving the dataset
        df.to_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/chicago-subset-cleaned.csv", index= False)

    @st.cache(persist= True)
    def load_data():
        df = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/chicago-subset-cleaned.csv")
        return df

    # Main panel
    st.subheader("**Dataset**")
    bigquery_check = st.sidebar.checkbox("Click here to see the original dataset from BigQuery!")
    if bigquery_check:
        st.info("Original Dataset from BigQuery!")
        Bigquery()

    og_check = st.sidebar.checkbox("Click to see the Cleaned dataset")
    if og_check:
        st.markdown("Cleaned dataset")
        df = load_data()
        st.write(df.head(1000))
        st.write(df.shape)
    
    maha_check = st.sidebar.checkbox("Maharashtra dataset")
    if maha_check:
        st.markdown("Synthetic dataset for Maharashtra")
        df_maha = pd.read_csv("/Users/devvratmungekar/OneDrive/Sem VII/BE Major Project/data/Maharashtra_Synthetic_dataset.csv")
        st.write(df_maha.head(1000))
        st.write(df_maha.shape)
      