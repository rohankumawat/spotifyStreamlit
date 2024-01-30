#######################################
#-------import packages---------------#
#######################################
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
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

#######################################
#-----------------title---------------#
#######################################
st.title(":smile_cat: Clutering")

#######################################
#-------K-means Clustering------------#
#######################################
def cluster(n_clusters, df):
    #######################################
    # Selecting the features for correlation analysis
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 
                'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    clustering_data = df[features]
    # Standardizing the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(scaled_data) # pass scaled data
    # Add cluster labels to the original data
    df['cluster'] = kmeans.labels_
    # Analyze the centroids
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)
    return kmeans, df, centroids

#######################################
#------------Plotting 2D--------------#
#######################################
def plot_clusters(df, n_clusters):
    # Selecting the features for correlation analysis
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 
                'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    
    # Call the cluster function to get the clustered data
    kmeans, df, centroids = cluster(n_clusters, df)

    # Apply PCA and reduce the data to two dimensions for visualization
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[features])

    # Create a DataFrame with the two principal components and the cluster labels
    df_pca = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2'])
    df_pca['cluster'] = df['cluster']

    # Create a color map
    color_map = px.colors.qualitative.Plotly

    # Create a scatter plot
    fig = px.scatter(df_pca, x='principal component 1', y='principal component 2', color='cluster', color_continuous_scale=px.colors.sequential.Plasma)

    # Calculate the centroids for the principal components
    centroids_pca = pca.transform(centroids)

    # Add centroid markers
    fig.add_trace(go.Scatter(
        x=centroids_pca[:, 0], 
        y=centroids_pca[:, 1],
        customdata=df[['name', 'artist_name']],
        mode='markers',
        marker=dict(
            size=10,
            color=[color_map[i % len(color_map)] for i in range(n_clusters)],
            symbol='x',
            line=dict(
                width=2,
            )
        ),
        name='centroids',
        hovertemplate='<b>{customdata[0]}<b><br><br>' + '{customdata[1]}',
    ))

    # fig.show()
    return fig

#######################################
#------------Plotting 3D--------------#
#######################################
def plot_clusters_3d(df, n_clusters):
    # Selecting the features for correlation analysis
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 
                'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    
    # Call the cluster function to get the clustered data
    kmeans, df, centroids = cluster(n_clusters, df)

    # Apply PCA and reduce the data to two dimensions for visualization
    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(df[features])

    # Create a DataFrame with the two principal components and the cluster labels
    df_pca = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2', 'principal component 3'])
    df_pca['cluster'] = df['cluster']

    # Calculate the centroids for the principal components
    centroids_pca = pca.transform(centroids)

    # Create a color map
    color_map = px.colors.qualitative.Plotly

    fig = px.scatter_3d(df_pca, x="principal component 1", y="principal component 2", z="principal component 3", color="cluster", color_continuous_scale=px.colors.sequential.Plasma)

    # Add centroid markers
    fig.add_trace(go.Scatter3d(
        x=centroids_pca[:, 0], 
        y=centroids_pca[:, 1],
        z=centroids_pca[:, 2],
        customdata=df[['name', 'artist_name']],
        mode='markers',
        marker=dict(
            size=5,
            color=[color_map[i % len(color_map)] for i in range(n_clusters)],
            symbol='x',
            line=dict(
                width=2,
            )
        ),
        name='centroids',
        hovertemplate='<b>{customdata[0]}<b><br><br>' + '{customdata[1]}',
    ))

    return fig

# slider for number of clusters
cluster_no = st.slider("Number of Clusters", 1, 25, 5) # initial cluter number is 5

# call the plot_clusters function
fig1 = plot_clusters(df, cluster_no)

# call the plot_clusters_3d function
fig2 = plot_clusters_3d(df, cluster_no)

# create two columns
# col1, col2 = st.columns(2)

# create two columns
tab1, tab2 = st.tabs(["Clustering 2D Graph", "Clustering 3D Graph"])

# display the plot
tab1.plotly_chart(fig1, use_container_width=True)

# display the plot
tab2.plotly_chart(fig2, use_container_width=True)