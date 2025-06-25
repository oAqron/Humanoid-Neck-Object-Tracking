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

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/<your-username>/humanoid-neck-tracker.git
   cd humanoid-neck-tracker
   ```

2. **Open in VS Code**:

   * Launch VS Code, choose **File > Open Folder**, select this project folder.
   * Ensure the Python interpreter is set to your `cv_env` virtual environment.

3. **Install dependencies**:

   ```bash
   python -m venv cv_env
   source cv_env/bin/activate   # or .\cv_env\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the demo**:

   ```bash
   python yolo_with_kalman.py
   ```

## Customization

* Edit `yolo_with_kalman.py` to adjust:

  * `proc_var`, `meas_var`, `dt` (Kalman tuning)
  * `Kp`, `current_pan` (control gain)
  * `send_pan_to_servo()` stub for your STM32 interfacing

## Next Steps

* Integrate STM32Cube HAL firmware for PWM servo control
* Map `current_pan` values into servo pulse widths
* Add multi-object tracking or ROS bridge as needed

---

© NTU Humanoid Robot Computer Vision Team
