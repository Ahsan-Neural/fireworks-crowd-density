import streamlit as st
import pandas as pd
import json
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.title("🎆 Fireworks Crowd Dashboard")

with open("output/ranking_output.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

spot_coordinates = {
    "spot_1": (24.8607, 67.0011),
    "spot_2": (24.8650, 67.0050),
    "spot_3": (24.8700, 67.0100)
}

user_location = (24.8550, 67.0300)

df["distance_km"] = df["spot_id"].map(
    lambda x: geodesic(user_location, spot_coordinates[x]).km
)

df["eta_minutes"] = (df["distance_km"] / 5) * 60

best_spot = df.sort_values(
    ["rank", "distance_km"]
).iloc[0]

st.subheader("Crowd Ranking")
st.dataframe(df)

st.subheader("Recommended Spot")
st.write(best_spot)

m = folium.Map(location=user_location, zoom_start=14)

folium.Marker(
    user_location,
    popup="You"
).add_to(m)

for spot, coords in spot_coordinates.items():
    folium.Marker(
        coords,
        popup=spot
    ).add_to(m)

st_folium(m)