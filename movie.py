import streamlit as st
import pandas as pd
# import joblib #to load the recommendation model

#model = joblib.load('your_model.pkl')

# title of the recommender app
# building the app with Sebastain & Mirella

st.title('Welcome to SMG Movies')
st.text('here we recommend movies based on user rating and popularity')

option = st.selectbox(
    'Please choose a movie')

# Add a footer to your app
st.text("Built with Streamlit")
