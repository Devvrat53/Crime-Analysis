import streamlit as st 
import base64

def app():
    st.title("Crime Analysis Web Application 👮🏻‍♀️🚨")
    #st.subheader("This is the web-application for analysing the data from the police record and provide meaning prediction from the same.")

    # GIF from Local system
    file_ = open("/Users/devvratmungekar/Downloads/1989_2019_permits.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(f'<img src= "data:image/gif;base64,{data_url}" alt= "cat.gif">', unsafe_allow_html= True)

