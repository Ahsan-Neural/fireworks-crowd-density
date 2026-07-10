import streamlit as st
import pandas as pd
import json
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Crowd Density Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #1c1f26;
    border: 1px solid #2a2e37;
    padding: 16px;
    border-radius: 10px;
}
div[data-testid="stMetricLabel"] { font-size: 14px; color: #9aa0aa; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("Fireworks Viewing Spot Recommender")
st.caption("Live crowd ranking and nearest-spot recommendation based on real-time head detection.")

with open("output/ranking_output.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["rank"] = df["rank"].astype(int)
df["spot_id"] = df["spot_id"].astype(str)
df["spot_name"] = df["spot_name"].astype(str)
df["head_count"] = df["head_count"].astype(int)
df["density"] = df["density"].fillna("N/A").astype(str)
df["crowd_level"] = df["crowd_level"].astype(str)

spot_coordinates = {
    "spot_1": (24.8607, 67.0011),
    "spot_2": (24.8650, 67.0050),
    "spot_3": (24.8700, 67.0100)
}
user_location = (24.8550, 67.0300)

df["distance_km"] = df["spot_id"].map(lambda x: round(geodesic(user_location, spot_coordinates[x]).km, 2))
df["eta_minutes"] = round((df["distance_km"] / 5) * 60, 1)

best_spot = df.sort_values(["rank", "distance_km"]).iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Recommended Spot", best_spot["spot_name"])
col2.metric("Crowd Level", best_spot["crowd_level"])
col3.metric("Estimated Walk Time", f"{best_spot['eta_minutes']} min")

st.divider()

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Spot Rankings")
    st.dataframe(
        df[["rank", "spot_name", "head_count", "crowd_level", "distance_km", "eta_minutes"]],
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("Live Map")
    m = folium.Map(location=user_location, zoom_start=14, tiles="cartodbpositron")
    folium.Marker(user_location, popup="You", icon=folium.Icon(color="blue")).add_to(m)
    for _, row in df.iterrows():
        color = "green" if row["crowd_level"] == "Low" else "orange" if row["crowd_level"] == "Moderate" else "red"
        folium.Marker(
            spot_coordinates[row["spot_id"]],
            popup=f"{row['spot_name']} — {row['crowd_level']}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    st_folium(m, use_container_width=True, height=420)