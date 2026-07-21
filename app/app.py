import streamlit as st
import pandas as pd

from data_loader import load_ranking_data
from recommendation import get_best_spot
from locations import SPOT_LOCATIONS
from map_utils import calculate_distance

st.set_page_config(
    page_title="Fireworks Crowd Density Estimator",
    layout="wide"
)

st.title("🎆 Fireworks Crowd Density Estimator")

ranking_data = load_ranking_data()
best_spot = get_best_spot(ranking_data)

st.subheader("🏆 Recommended Spot")

st.success(
    f"""
    **{best_spot['spot_name']}**

    Crowd Level: {best_spot['crowd_level']}

    Head Count: {best_spot['head_count']}
    """
)
# 👇 Add this
location = SPOT_LOCATIONS.get(best_spot["spot_id"])

st.subheader("📍 Spot Location")

st.write(f"Latitude: {location['latitude']}")
st.write(f"Longitude: {location['longitude']}")

# 👇 Then distance calculation
user_location = (24.8585, 67.0099)

spot_location = (
    location["latitude"],
    location["longitude"]
)

distance = calculate_distance(user_location, spot_location)

st.subheader("📏 Distance")

st.info(f"{distance} km")


location = SPOT_LOCATIONS.get(best_spot["spot_id"])

st.subheader("📍 Spot Location")

st.write(f"Latitude : {location['latitude']}")
st.write(f"Longitude : {location['longitude']}")

df = pd.DataFrame(ranking_data)

# Replace missing density values
df["density"] = df["density"].fillna("N/A")

st.subheader("Spot Rankings")

st.dataframe(
    df[["rank", "spot_name", "head_count", "crowd_level"]],
    use_container_width=True,
    hide_index=True
)

