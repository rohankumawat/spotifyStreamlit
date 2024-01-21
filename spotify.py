# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:09:10 2022

@author: DAZZ
"""

# import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st

##################################################################
#default streamlit settings
##################################################################

# wide page layout
st.set_page_config(layout="wide")

# hide the menu button
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# from datetime import datetime

##################################################################
# define functions
##################################################################

def overallGraph(data):
    fig = make_subplots(rows = 4 , cols = 3,
                    specs=[[{}, {}, {}],
                           [{}, {}, {}],
                           [{}, {}, {}],
                           [{}, {}, {}]],
                   subplot_titles=["Acousticness", "Danceability", "Energy", "Instrumentalness",
                                  "Liveness", "Loudness", "Speechiness", "Tempo", "Valence",
                                  "Mode", "Explicit", "Popularity"]) 
    trace1 = go.Histogram(x=data["acousticness"],
            nbinsx=45, showlegend=False) 
    trace2 = go.Histogram(x=data["danceability"],
            nbinsx=45, showlegend=False) 
    trace3 = go.Histogram(x=data["energy"],
            nbinsx=45, showlegend=False) 
    trace4 = go.Histogram(x=data["instrumentalness"],
            nbinsx=45, showlegend=False) 
    trace5 = go.Histogram(x=data["liveness"],
            nbinsx=45, showlegend=False) 
    trace6 = go.Histogram(x=data["loudness"],
            nbinsx=45, showlegend=False) 
    trace7 = go.Histogram(x=data["speechiness"],
            nbinsx=45, showlegend=False) 
    trace8 = go.Histogram(x=data["tempo"],
            nbinsx=45, showlegend=False) 
    trace9 = go.Histogram(x=data["valence"],
            nbinsx=45, showlegend=False) 
    trace10 = go.Histogram(x=data["mode"], showlegend=False) 
    trace11 = go.Histogram(x=data["explicit"], showlegend=False) 
    trace12 = go.Histogram(x=data["popularity"],
            nbinsx=45, showlegend=False) 
    fig.append_trace(trace1, 1, 1) 
    fig.append_trace(trace2, 1, 2) 
    fig.append_trace(trace3, 1, 3) 
    fig.append_trace(trace4, 2, 1) 
    fig.append_trace(trace5, 2, 2) 
    fig.append_trace(trace6, 2, 3) 
    fig.append_trace(trace7, 3, 1) 
    fig.append_trace(trace8, 3, 2) 
    fig.append_trace(trace9, 3, 3) 
    fig.append_trace(trace10, 4, 1) 
    fig.append_trace(trace11, 4, 2) 
    fig.append_trace(trace12, 4, 3)
    
    fig.update_layout(height = 700, width = 1200, autosize=True,
                      title={
                    'text': "Distribution of Features",
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
    
    return fig

if "function" not in st.session_state:
    st.session_state["function"] = overallGraph

##################################################################
# load data
##################################################################
@st.cache_data
def load_data():
    df = pd.read_csv('spotify15k.csv')
    df.drop(["Unnamed: 0", "Unnamed: 0.1", "track_number"], axis=1, inplace=True)
    return df

@st.cache_data
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')


# Load data and store in session_state if not already loaded
if 'df' not in st.session_state:
    df = load_data()
    st.session_state['df'] = df
if 'download_df' not in st.session_state:
    download_df = convert_df(st.session_state['df'])
    st.session_state['download_df'] = download_df

# artist
artList = df['artist_name'].unique()
artList = artList.tolist()
artList.insert(0, "Overall")

# album
albList = df['album'].unique()
albList = albList.tolist()
albList.insert(0, "Overall")

# Check if the session state variable exists, if not, then assign it
if 'artList' not in st.session_state:
    st.session_state['artList'] = artList

if 'albList' not in st.session_state:
    st.session_state['albList'] = albList