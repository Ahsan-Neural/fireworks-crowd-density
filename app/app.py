import streamlit as st
import pandas as pd

from data_loader import load_ranking_data
from recommendation import get_best_spot
from locations import SPOT_LOCATIONS
from map_utils import calculate_distance, calculate_walking_time
from map_view import create_map
from streamlit_folium import st_folium


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Fireworks Crowd Density Estimator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Fireworks Crowd Density Estimator")
st.caption("Real-time crowd density comparison and viewing spot recommendation system")
st.divider()


# -------------------------------
# Load Data
# -------------------------------

try:
    ranking_data = load_ranking_data()

    if not ranking_data:
        st.error("No ranking data found.")
        st.stop()

    best_spot = get_best_spot(ranking_data)

except Exception as e:
    st.error("Failed to load crowd ranking data.")
    st.write(e)
    st.stop()

location = SPOT_LOCATIONS.get(best_spot["spot_id"])

if location is None:
    st.error("Location data not found for recommended spot.")
    st.stop()

user_location = (24.8585, 67.0099)

spot_location = (
    location["latitude"],
    location["longitude"]
)

try:
    distance = calculate_distance(
        user_location,
        spot_location
    )

    walking_time = calculate_walking_time(distance)

except Exception:
    st.error("Unable to calculate distance.")
    st.stop()
walking_time = calculate_walking_time(distance)


# -------------------------------
# Dashboard Metrics
# -------------------------------

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    st.metric("Best Spot", best_spot["spot_name"])

with col2:
    st.metric(
        "Distance",
        f"{distance} km",
        f"🚶 {walking_time} min walk"
    )

with col3:
    st.metric("Head Count", best_spot["head_count"])

st.divider()


# -------------------------------
# Recommended Spot
# -------------------------------

st.subheader("Recommended Spot")

with st.container(border=True):

    st.markdown(f"### {best_spot['spot_name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Crowd Level:** {best_spot['crowd_level']}")
        st.write(f"**Head Count:** {best_spot['head_count']}")

    with col2:
        st.write(f"**Distance:** {distance} km")
        st.write(f"**Walking Time:** {walking_time} minutes")
        st.write(f"**Latitude:** {location['latitude']:.4f}")
        st.write(f"**Longitude:** {location['longitude']:.4f}")

st.divider()
# -------------------------------
# Interactive Map
# -------------------------------

st.divider()

st.subheader("🗺️ Viewing Spots Map")

map_object = create_map(
    user_location,
    SPOT_LOCATIONS,
    best_spot["spot_id"],
    ranking_data
)

st_folium(
    map_object,
    width=900,
    height=500
)

# -------------------------------
# Crowd Ranking
# -------------------------------

df = pd.DataFrame(ranking_data)

st.subheader("Crowd Ranking")
st.caption("Viewing spots ranked from least crowded to most crowded")

def crowd_badge(level):

    colors = {
        "Low": "🟢",
        "Moderate": "🟡",
        "High": "🟠",
        "Very High": "🔴"
    }

    return f"{colors.get(level, '⚪')} {level}"


df["crowd_level"] = df["crowd_level"].apply(crowd_badge)


st.dataframe(
    df[["rank", "spot_name", "head_count", "crowd_level"]],
    use_container_width=True,
    hide_index=True,
    height=180
)

