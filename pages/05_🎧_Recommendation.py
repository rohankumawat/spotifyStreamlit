import streamlit as st
import sys
from pathlib import Path
from sklearn.cluster import KMeans 
#Progreebar
from tqdm import tqdm
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
load_dotenv()

# Get the parent directory
parent_dir = str(Path(__file__).parent.parent)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from Spotify import df, download_df, artList, albList, overallGraph

# set up Spotipy
client_id = os.getenv("client_id")
print(client_id)
client_secret = os.getenv("client_secret")
print(client_secret)
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

st.title(":smile_cat: Recommendation")


# remove the square brackets from the artists
df["artist_name"]=df["artist_name"].str.replace("[", "")
df["artist_name"]=df["artist_name"].str.replace("]", "")
df["artist_name"]=df["artist_name"].str.replace("'", "")

# normalise the columns in the dataframe
def normalize_column(col):
    max_d = df[col].max()
    min_d = df[col].min()
    df[col] = (df[col] - min_d)/(max_d - min_d)

# normalize all of numerical columns so that min value is 0 and max value is 1
num_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
num = df.select_dtypes(include=num_types)

for col in num.columns:
    normalize_column(col)

#perform Kmeans Clustering
km = KMeans(n_clusters=5, n_init=10)
pred = km.fit_predict(num)
df['pred'] = pred
normalize_column('pred')

# neighbourhood based collborative filterng recommendation system using similarity metrics
# manhattan distance is calculated for all songs and recommend songs that are similar to it, based on any given song
class recommendSongs():
    
    def __init__(self, data):
        self.data_ = data
    
    #function which returns recommendations, we can also choose the amount of songs to be recommended
    def get_recommendations(self, song_name, n_top):
        distances = []
        #choosing the given song_name and dropping it from the data
        song = self.data_[(self.data_.name.str.lower() == song_name.lower())].head(1).values[0]
        remData = self.data_[self.data_.name.str.lower() != song_name.lower()].copy()
        for recSong in tqdm(remData.values):
            dist = 0
            for col in np.arange(len(remData.columns)):
                #indices of non-numerical columns(id, uri, name, artists, album)
                if not col in [0,1,2,3,4,14]:
                    #calculating the manhettan distances for each numerical feature
                    dist = dist + np.absolute(float(song[col]) - float(recSong[col]))
            distances.append(dist)
        remData['distance'] = distances
        #sorting our data to be ascending by 'distance' feature
        remData = remData.sort_values('distance')
        columns = ['artist_name', 'name']
        return remData[columns][:n_top]

#Instantiate recommender class
recommender = recommendSongs(df)

song_list = df['name'].tolist()

selected_song = st.selectbox("Select a song", song_list)

# After the song is selected, find its URI in the DataFrame
selected_song_uri = df.loc[df['name'] == selected_song, 'id'].values[0]
recommendations = sp.recommendations(seed_tracks=[selected_song_uri], limit=5)
# Create empty list to store the artist names and song names
data = []
# add the data to the list
for track in recommendations['tracks']:
    data.append([track['artists'][0]['name'], track['name']])
# Create a DataFrame from the list
df_inbuilt = pd.DataFrame(data, columns=['Artist', 'Track'])

col1, col2 = st.columns(2)
with col1:
    st.title("In-built Song Recommender")
    st.dataframe(df_inbuilt, 
                 hide_index=True, 
                 use_container_width=True)
with col2:
    st.title("Spotify Song Recommender")
    st.dataframe(recommender.get_recommendations(song_name=selected_song, n_top=5), 
                 column_config={
                     "artist_name": "Artist",
                     "name": "Track"
                 },
                 hide_index=True, 
                 use_container_width=True)