import streamlit as st
import pandas as pd

from data_loader import load_ranking_data


st.set_page_config(
    page_title="Fireworks Crowd Density Estimator",
    layout="wide"
)

st.title("🎆 Fireworks Crowd Density Estimator")

ranking_data = load_ranking_data()

df = pd.DataFrame(ranking_data)

st.subheader("Spot Rankings")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)