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

def artis(artist):
    # extract artist details
    df_art = df[df["artist_name"] == artist]
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


df = load_data()
download_df = convert_df(df)

##################################################################
# engineer data
##################################################################

# overall metrics columns
songsCount = df.shape[0]
artistsCount = len(df.artist_name.unique())
albumCount = len(df.album.unique())

# dropdown
features = ['overall', 'acousticness', 'danceability', 'energy', 'instrumentalness',
            'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 
            'explicit', 'mode', 'popularity']

features_info = {'acousticness': 'A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.',
                 'danceability': 'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable',
                 'energy': 'Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.',
                 'instrumentalness': 'Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.',
                 'liveness': 'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.',
                 'loudness': 'The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.',
                 'speechiness': 'Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.',
                 'tempo': 'The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.',
                 'valence': 'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).',
                 'explicit': 'An explicit track is one that has curse words or language or art that is sexual, violent, or offensive in nature.',
                 'mode': 'Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.',
                 'popularity': 'Popularity of the track (The higher, the more popular it is)'}

# artist
artList = df['artist_name'].unique()
artList = artList.tolist()
artList.insert(0, "Overall")

# album
albList = df['album'].unique()
albList = albList.tolist()
albList.insert(0, "Overall")

##################################################################
# build dashboard
##################################################################

# sidebar

add_sidebar = st.sidebar.selectbox('Analysis', ('Overall Metrics', 'Artist Analysis', 'Album Analysis', 'Clustering', 'Recommendation System'))

# total picture

##################################################################
# OVERALL SIDEBAR SELECT
##################################################################
if add_sidebar == "Overall Metrics":
    st.title(":smile_cat: Spotify Analysis")
    
    # explanation
    st.text("Spotify is an audio streaming and media services provider. It is one of the largest music streaming service providers, with over 406 Million monthly active users.")
    with st.expander("Click for more information:"):
        st.markdown("""
                    The __Web App__ shows an in-depth analysis of the Spotify Dataset. 
                    
                    It is divided into multiple parts: __Overall Analysis__, __Artist Analysis__, __Album Analysis__, __Clustering__, and __Recommendation Engine__. 
                    
                    - Overall Metrics presents an overall summary of songs and the features that Spotify stores.
                    
                    - Artist Analysis shows every artists' statistics.
                    
                    - The Album Analysis page contains information on albums and songs.""")
                    
        st.download_button(
            label="To work on the dataset, click on this to Downlaod",
            data=download_df,
            file_name='spotify.csv',
            mime='text/csv',
            )
    
    # showing dataset details
    col1, col2, col3 = st.columns(3)
    
    col1.metric("No. of Artists", artistsCount)
    col2.metric("No. of Albums", albumCount)
    col3.metric("No. of Songs", songsCount)
    
    # dropdown
    feature_select = st.selectbox('Features of Songs stored by Spotify. Pick a Feature (To know about each feature in depth):', features)
    with st.expander("Click to know about Features:"):
        st.markdown("""
                    __Spotify__ is known for its algorithm, the main outstanding point of the streaming giant to its competitors. 
                    The algorithm constantly finds new ways to understand the kind of music one listens to and analyses the reason 
                    behind a person listening to a particular song or preferring a particular genre. 
                    Spotify stores data of artists, albums, songs, and users and relies on its algorithm, unlike any other music streaming service, 
                    to achieve all of the abovementioned things. When it comes to songs, it stores some song features and strongly analyses all of the songs. 
                    
                    I've extracted out songs features using the __Spotify API__. The graph below shows the distribution of the song's features (Basically, where do songs' features lie in a specific range).
                    """)
    # features information
    if feature_select == "overall":
        st.header(":star: Overall Summary")
        # display only those which have the highest popularity
        df_90 = df.loc[df["popularity"]>=90, ["album", "artist_name", "name", "popularity"]] 
        df_90.sort_values("popularity", inplace=True, ascending=False)
        df_90.reset_index(drop=True, inplace=True)
        st.write("Top songs in the dataset (currently). [Filtered by Popularity]")
        st.dataframe(df_90)
        # st.dataframe(df_90.style.highlight_max(axis=0))
        # th_props = [('background', '#7CAE00'), 
        #          ('color', 'white'),
        #          ('font-family', 'verdana')]
        # td_props = [('font-family', 'verdana')]
        # tr_odd = [('background', '#DCDCDC')]
        # tr_even = [('background', 'white')]
        # tr_hover = [('background-color', 'yellow')]
        # styles = [
        #    dict(selector="th", props=th_props),
        #    dict(selector="td", props=td_props),
        #   dict(selector="tr:nth-of-type(odd)", props=tr_odd),
        #    dict(selector="tr:nth-of-type(even)", props=tr_even),
        #    dict(selector="tr:hover", props=tr_hover)]
        st.plotly_chart(overallGraph(df))
            
    else:
        col1, col2 = st.columns(2) 
        with col1:
            st.header(feature_select.capitalize())
            # st.text(features_info[feature_select]) NOOO TEXT WRAP
            st.write(features_info[feature_select].capitalize()) 
        with col2: 
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

##################################################################    
# ARTIST SIDEBAR SELECT
##################################################################
            
if add_sidebar == "Artist Analysis":
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

##################################################################
# ALBUM ANALYSIS SELECT
##################################################################
                
if add_sidebar == "Album Analysis":
    st.title(":smile_cat: Album Analysis")

    album_select = st.selectbox('Pick an Album: ', albList)

    if album_select == "Overall":
        st.title(":star: Summary of Artists")

        # total number of songs per album
        songXalbCount = df['album'].value_counts()
        songXalbCount = songXalbCount.to_frame().reset_index()
        songXalbCount_15 = songXalbCount.head(15)
        print(songXalbCount_15)
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
        
        st.plotly_chart(fig)

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
        st.plotly_chart(overallGraph(df_alb))

##################################################################
# CLUSTERING SELECT
##################################################################
    
if add_sidebar == "Clustering":
    st.title(":smile_cat: Clustering")
    
    st.write("CURRENTLY WORKING ON IT! 	:crying_cat_face: 	:crying_cat_face: 	:crying_cat_face:")

##################################################################    
# RECOMMENDATION SYSTEM SELECT
##################################################################
    
if add_sidebar == "Recommendation System":
    st.title(":smile_cat: Recommendation System")
    
    st.write("CURRENTLY WORKING ON IT! 	:crying_cat_face: 	:crying_cat_face: 	:crying_cat_face:")