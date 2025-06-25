# Humanoid Neck Object-Tracking

This repository contains the Computer Vision pipeline and Kalman-filter-based control loop to enable a humanoid robot's neck to follow detected objects in real-time.

## Project Structure

```
├── yolo_with_kalman.py    # Main detection + filtering + control demo
├── find_all_cams.py       # Utility to enumerate camera indices and backends
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Features

* **USB Camera Capture** at 1280×720 via OpenCV
* **YOLOv8-nano** object detection with Ultralytics
* **1D Kalman Filter** (position + velocity) for smooth, predictive tracking
* **Proportional Control** stub for sending pan commands to actuators
---

© NTU Humanoid Robot Computer Vision Team
