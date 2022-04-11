# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:09:10 2022

@author: DAZZ
"""

# import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
# from datetime import datetime

# define functions

# load data
@st.cache
def load_data():
    df = pd.read_csv('spotify15k.csv')
    df.drop(["Unnamed: 0", "Unnamed: 0.1", "track_number"], axis=1, inplace=True)
    return df

df = load_data()
# engineer data

# overall metrics columns
songsCount = df.shape[0]
artistsCount = len(df.artist_name.unique())
albumCount = len(df.album.unique())

# dropdown
features = ['acousticness', 'danceability', 'energy', 'instrumentalness',
            'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 
            'explicit', 'mode', 'popularity']

# build dashboard

add_sidebar = st.sidebar.selectbox('Analysis', ('Overall Metrics', 'Artist Analysis'))

# total picture

if add_sidebar == "Overall Metrics":
    st.title(":smile_cat: Overall Metrics")
    
    # showing dataset details
    
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    col1.metric("Artists", artistsCount)
    col2.metric("Albums", albumCount)
    col3.metric("Songs", songsCount)
    
    # dropdown
    st.write("Features of Songs stored by Spotify")
    feature_select = st.selectbox('Pick a Feature:', features)
    # features information
    fig = px.histogram(df, 
                       x=feature_select,
                       nbins=45,
                       marginal='box')
    fig.update_traces(marker_line_color='black',
                      marker_line_width=1.2)
    fig.update_layout(uniformtext_minsize=14,
                      uniformtext_mode="hide",
                      legend={'x':0, 'y':1.0})
    st.plotly_chart(fig)
    
if add_sidebar == "Artist Analysis":
    st.title("Artist Analysis")