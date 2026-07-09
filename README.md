# Fireworks Crowd Density Estimator

A real-time crowd density comparison system for fireworks viewing spots. Detects and counts people across multiple camera feeds using a fine-tuned YOLO26n head detector, then ranks viewing spots from least to most crowded to recommend better alternatives.

## Project Status

Head detection model trained and evaluated. Multi-feed ranking engine and Streamlit dashboard in progress.

## Problem

Crowd density estimation is a solved research problem, but no existing system combines real-time multi-camera density comparison with actionable spot recommendations for transient, single-night outdoor events like fireworks displays. Consumer apps rely on historical footfall data tied to permanent venues; this project works from live camera feeds alone, with no prior calibration or history required.

## Architecture
Camera Feeds → Frame Grabber (OpenCV) → Preprocessing (low-light correction)
→ YOLO26n Head Detector → Density Normalization (homography)
→ Ranking Engine → Recommendation Logic (distance + ETA)
→ Streamlit Dashboard

text

## Model Results

Fine-tuned YOLO26n on the RPEE-Heads dataset (1,346 training images, 109,913 head annotations from railway platforms and event entrances).

| Metric | Score |
|---|---|
| Precision | 0.874 |
| Recall | 0.729 |
| mAP50 | 0.809 |
| mAP50-95 | 0.443 |

Training curves:

![Training Results](results/results.png)

Confusion matrix:

![Confusion Matrix](results/confusion_matrix.png)

Precision-recall curve:

![PR Curve](results/BoxPR_curve.png)

Sample detection on a low-light outdoor scene:

![Sample Prediction](results/sample_prediction_night.jpg)

## Dataset

[RPEE-Heads](https://doi.org/10.34735/ped.2024.2) — Railway Platforms and Event Entrances Heads dataset, licensed CC BY-SA 4.0. Not redistributed here due to size and licensing; download instructions are in the training notebook.

## Repository Structure
├── notebooks/ Training notebook
├── models/ Trained model weights
├── configs/ Dataset YAML config
├── docs/ Model info and metrics
├── results/ Training curves, evaluation plots, sample predictions

text

## Usage

```python
from ultralytics import YOLO

model = YOLO("models/head_detector_yolo26n.pt")
results = model.predict(source="your_image.jpg", conf=0.3)
```

## Requirements
ultralytics

text

## License

Code is licensed under MIT. The trained model weights inherit the CC BY-SA 4.0 share-alike condition from the RPEE-Heads dataset used for fine-tuning.

## Credits

- [RPEE-Heads Dataset](https://arxiv.org/abs/2411.18164) — Boltes et al., 2024
- [Ultralytics YOLO26](https://docs.ultralytics.com/models/yolo26)
