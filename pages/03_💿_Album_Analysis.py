import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import sys
from pathlib import Path

# Get the parent directory
parent_dir = str(Path(__file__).parent.parent)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from Spotify import df, download_df, artList, albList, overallGraph

def albu(album):
    # Extract album details
    df_alb = df[df["album"] == album]
    
    # Sorting the songs based on popularity
    df_alb.sort_values('popularity', ascending=False, inplace=True)
    
    # Reset the index of the sorted DataFrame
    df_alb.reset_index(drop=True, inplace=True)
    
    # Count the number of songs in the album
    couSong = len(df_alb)
    
    # Calculate the average duration of songs in the album
    avg_dura = int(df_alb.duration_ms.mean())
    
    # Calculate the average popularity of songs in the album
    avg_popu = int(df_alb.popularity.mean())
    
    return df_alb, couSong, avg_dura, avg_popu

st.title(":smile_cat: Album Analysis")

album_select = st.selectbox('Pick an Album: ', albList)

if album_select == "Overall":
    st.title(":star: Summary of Artists")

    # total number of songs per album
    songXalbCount = df['album'].value_counts()
    songXalbCount = songXalbCount.to_frame().reset_index()
    songXalbCount_15 = songXalbCount.head(15)
    # print(songXalbCount_15)
    # displaying graph no. 1
    fig = px.bar(songXalbCount_15,
            x="count",
            y="album",
            color='count',
            opacity=0.9,
        color_continuous_scale=px.colors.sequential.Peach,
        range_color=[40, 50],
        text='count',
        hover_name="count",
        labels={"album":"Album Name", "count": "Number of Songs"},
        template="plotly_white")
    
    fig.update_traces(marker_line_color='black',
                        marker_line_width=1.5)
    
    fig.update_layout(uniformtext_minsize=14,
                uniformtext_mode="hide",
                height = 700, width = 1200,
                legend={'x':0,'y':1.0},
                title={
                'text': "Number of Songs per Album",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}
                )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.header(album_select)

    # retreive album's information
    df_alb, couSong, avg_dura, avg_popu = albu(album_select)

    # showing album details
    col1, col2 = st.columns(2)
    col1.metric("No. of Songs", couSong)
    col2.metric("Average Duration", avg_dura)

    col1, col2 = st.columns(2)
    col2.metric("Average Popularity", avg_popu)
    with col1:
        st.title("Top 5 Songs")
        st.dataframe(df_alb.loc[0:5, ["name", "popularity", "duration_ms"]])
    
    # displaying features of the artist
    st.plotly_chart(overallGraph(df_alb), use_container_width=True)