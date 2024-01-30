import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import sys
from pathlib import Path

# Get the parent directory
parent_dir = str(Path(__file__).parent.parent)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from spotify import df, download_df, artList, albList, overallGraph

st.title(":smile_cat: Spotify Analysis")

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

# dataset details
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
    st.plotly_chart(overallGraph(df))
        
else:
    col1, col2 = st.columns(2) 
    with col1:
        st.header(feature_select.capitalize())
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