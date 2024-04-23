# DBSCAN clustering
from sklearn.cluster import DBSCAN
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import streamlit as st
df = pd.read_csv('traffy_flood.csv')

coords = df[['latitude', 'longitude']]

db = DBSCAN(eps=0.005, min_samples=10).fit(coords)
df['cluster'] = db.labels_
# Filter out noise points
df = df[df['cluster'] != -1]
# Count the number of points in each cluster
clusters_count = df['cluster'].value_counts()
# Exclude the '-1' cluster, which represents noise
clusters_count = clusters_count[clusters_count.index != -1]
unique_clusters = df['cluster'].unique()
num_clusters = len(unique_clusters)

# Use a continuous colormap to generate colors, ensure we have enough colors for all clusters.
colormap = plt.get_cmap('hsv')
cluster_colors = {cluster: [int(x*255) for x in colormap(i/num_clusters)[:3]] for i, cluster in enumerate(unique_clusters)}
# Map cluster ID to color for each row in the dataframe
df['color'] = df['cluster'].map(cluster_colors)


# Define the scatter plot layer
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[longitude, latitude]",
    get_color='color',
    get_radius=200,
    opacity=0.5,
    pickable=True
)
view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=10
)   

map = pdk.Deck(layers=[scatter_layer], initial_view_state=view_state, tooltip={"text": "{cluster}\n{subdistrict} {district}\n{timestamp}"})

st.pydeck_chart(map)
