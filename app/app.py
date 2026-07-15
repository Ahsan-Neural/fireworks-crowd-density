import os
import streamlit as st
import pandas as pd
import json
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO

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

st.title("Fireworks Crowd Density Dashboard")
st.caption("Real-time head detection and crowd ranking for fireworks viewing spots.")

@st.cache_resource
def load_model():
    model_path = "models/head_detector_yolo26n.pt"
    if not os.path.exists(model_path):
        st.error(f"Model file not found: {model_path}")
        st.stop()
    return YOLO(model_path)

model = load_model()

def draw_density_grid(frame, boxes, grid_size=8):
    h, w = frame.shape[:2]
    cell_h, cell_w = h // grid_size, w // grid_size
    grid_counts = np.zeros((grid_size, grid_size))

    for box in boxes:
        x_center = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
        y_center = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
        col = min(int(x_center // cell_w), grid_size - 1)
        row = min(int(y_center // cell_h), grid_size - 1)
        grid_counts[row, col] += 1

    overlay = frame.copy()
    max_count = grid_counts.max() if grid_counts.max() > 0 else 1

    for row in range(grid_size):
        for col in range(grid_size):
            intensity = grid_counts[row, col] / max_count
            if intensity > 0:
                color = (0, int(255 * (1 - intensity)), int(255 * intensity))
                x1, y1 = col * cell_w, row * cell_h
                x2, y2 = x1 + cell_w, y1 + cell_h
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)

    blended = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)
    return blended


tab1, tab2 = st.tabs(["Spot Rankings", "Live Detection"])

with tab1:
    with open("output/ranking_output.json", "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["rank"] = df["rank"].astype(int)
    df["spot_id"] = df["spot_id"].astype(str)
    df["spot_name"] = df["spot_name"].astype(str)
    df["head_count"] = df["head_count"].astype(int)
    df["density"] = df["density"].fillna("N/A").astype(str)
    df["crowd_level"] = df["crowd_level"].astype(str)

    best_spot = df.sort_values(["rank"]).iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Recommended Spot", best_spot["spot_name"])
    col2.metric("Crowd Level", best_spot["crowd_level"])
    col3.metric("Head Count", int(best_spot["head_count"]))

    st.divider()

    st.subheader("Spot Rankings")
    st.dataframe(
        df[["rank", "spot_name", "head_count", "crowd_level"]],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.subheader("Upload Image or Video for Real-Time Detection")
    mode = st.radio("Input type", ["Image", "Video"], horizontal=True)

    if mode == "Image":
        uploaded_file = st.file_uploader("Upload crowd image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tfile.write(uploaded_file.read())

            results = model.predict(source=tfile.name, conf=0.3, verbose=False)
            annotated = results[0].plot()
            head_count = len(results[0].boxes)

            col1, col2 = st.columns(2)
            with col1:
                st.image(annotated, channels="BGR", caption="Bounding Box Detection", use_container_width=True)
            with col2:
                heatmap_frame = draw_density_grid(results[0].orig_img.copy(), results[0].boxes)
                st.image(heatmap_frame, channels="BGR", caption="Density Heatmap", use_container_width=True)

            st.metric("Head Count", head_count)

    else:
        uploaded_file = st.file_uploader("Upload crowd video", type=["mp4", "mov", "avi"])
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tfile.write(uploaded_file.read())

            cap = cv2.VideoCapture(tfile.name)
            stframe = st.empty()
            count_display = st.empty()
            counts_over_time = []

            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                results = model.predict(frame, conf=0.3, verbose=False)
                annotated_frame = results[0].plot()
                head_count = len(results[0].boxes)
                counts_over_time.append(head_count)

                stframe.image(annotated_frame, channels="BGR", use_container_width=True)
                count_display.metric("Current Head Count", head_count)

            cap.release()

            if counts_over_time:
                st.line_chart(counts_over_time)
                st.caption("Head count over time across the video.")
