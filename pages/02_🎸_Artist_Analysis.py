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

from spotify import df, artList, overallGraph

def artis(artist):
    # extract artist details
    df_art = df[df["artist_name"] == artist].copy()
    df_art.sort_values('popularity', ascending=False, inplace=True)
    df_art.reset_index(drop=True, inplace=True)
    # popular album
    popAlb = df_art.groupby("album").popularity.mean()
    popAlb = popAlb.to_frame().reset_index()
    popAlb["popularity"] = popAlb["popularity"].astype(int)
    # count album
    couAlb = len(df_art.album.unique())
    # songs count
    couSon = len(df_art)
    # avg duration of songs
    avg_dur = df_art.duration_ms.mean()
    # avg popularity of songs
    avg_pop = df_art.popularity.mean()
    return df_art, popAlb, couAlb, couSon, avg_dur, avg_pop

st.title(":smile_cat: Artist Analysis")
# st.snow()
# dropdown
artist_select = st.selectbox('Pick an Artist: ', artList)

if artist_select == "Overall":
    st.title(":star: Summary of Artists")
    # total number of songs per artist
    songXartCount = df['artist_name'].value_counts()
    songXartCount = songXartCount.to_frame().reset_index()
    # songXartCount = songXartCount.rename(columns={"index": "artist_name", "artist_name": "count"})
    songXartCount_15 = songXartCount.head(15)
    # print(songXartCount_15)
    # displaying graph no. 1
    fig = px.bar(songXartCount_15,
            x="count",
            y="artist_name",
            color='count',
            opacity=0.9,
        color_continuous_scale=px.colors.sequential.Peach,
        range_color=[200, 700],
        text='count',
        hover_name="count",
        labels={"artist_name":"Artist Name", "count": "Number of Songs"},
        template="plotly_white")

    fig.update_traces(marker_line_color='black',
                        marker_line_width=1.5)

    fig.update_layout(uniformtext_minsize=14,
                uniformtext_mode="hide",
                height = 700, width = 1200,
                legend={'x':0,'y':1.0},
                title={
                'text': "Number of Songs per Artist",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}
                )
    st.plotly_chart(fig)
    
    # total number of albums per artist
    albXart = df.groupby('artist_name').album.unique()
    # converting the series to dataframe
    albXart = pd.DataFrame({'artist_name':albXart.index, 'albums':albXart.values})
    # creating an empty list to store out count values
    countL = []
    # appending the count of every column to the empty list
    for i in albXart.albums:
        countL.append(i.size)
        # adding another column to the dataframe
    albXart['count'] = countL
    albXart = albXart.sort_values(by="count", ascending=False).reset_index(drop=True)
    # displaying graph no. 2
    fig = px.bar(albXart.loc[0:15],
            x="count",
            y="artist_name",
            color='count',
            opacity=0.9,
        color_continuous_scale=px.colors.sequential.Peach,
        range_color=[0, 25],
        text='count',
        hover_name="count",
        labels={"artist_name":"Artist Name", "count": "Number of Albums"},
        template="plotly_white")

    fig.update_traces(marker_line_color='black',
                marker_line_width=1.5)

    fig.update_layout(uniformtext_minsize=14,
                uniformtext_mode="hide",
                legend={'x':0,'y':1.0},
                height = 700, width = 1200,
                title={
                'text': "Number of Albums per Artist",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}
                )
    st.plotly_chart(fig)

else:
    st.header(artist_select)
    
    # retreive artist's information 
    df_art, popAlb, couAlb, couSon, avg_dur, avg_pop = artis(artist_select)
    
    # showing artist details
    col1, col2 = st.columns(2)
    col1.metric("No. of Albums", couAlb)
    col2.metric("No. of Songs", couSon)
    
    col1, col2 = st.columns(2)
    col1.metric("Most Popular Album", popAlb.loc[0].album, delta=int(popAlb.loc[0].popularity))
    col2.metric("Most popular Song", df_art.loc[0]['name'], delta=int(df_art.loc[0]['popularity']))
        
    # displaying top 5 songs and top albums of the artist
    col1, col2 = st.columns(2)
    with col1:
        st.title("Top 5 Songs")
        st.dataframe(df_art.loc[0:5, ["name", "popularity", "duration_ms"]])
    with col2:
        st.title("Top Albums")
        st.dataframe(popAlb)
    
    # displaying features of the artist
    st.plotly_chart(overallGraph(df_art))