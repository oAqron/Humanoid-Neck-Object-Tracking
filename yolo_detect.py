import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

# --- Kalman Filter setup for 1D position+velocity ---
kf = cv2.KalmanFilter(2, 1)
dt = 1/20  # approximate frame interval (seconds)
kf.transitionMatrix = np.array([[1, dt],
                                [0,  1]], np.float32)
kf.measurementMatrix = np.array([[1, 0]], np.float32)
proc_var = 0.5
kf.processNoiseCov = proc_var * np.array([
    [dt**4 / 4, dt**3 / 2],
    [dt**3 / 2, dt**2]
], np.float32)
meas_var = 50.0
kf.measurementNoiseCov = np.array([[meas_var]], np.float32)
kf.errorCovPre = np.eye(2, dtype=np.float32)
initial_center = 1280 / 2
kf.statePre = np.array([[initial_center], [0]], np.float32)

# --- Data logging setup ---
raw_xs = []
filt_xs = []
timestamps = []
frame_idx = 0

# Initialize camera
cam_index = 0
cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if not cap.isOpened():
    raise IOError(f"Cannot open camera at index {cam_index}")

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Control parameters
Kp = 0.02
current_pan = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # YOLO inference
    results = model(frame)[0]

    # Default: no measurement this frame
    measured = False

    # If detection found, take first box’s center
    if len(results.boxes) > 0:
        x1, y1, x2, y2 = map(int, results.boxes.xyxy[0].cpu().numpy())
        cx = (x1 + x2) / 2.0
        kf.correct(np.array([[np.float32(cx)]]))
        measured = True

    # Predict step
    pred = kf.predict()
    pred_cx = pred[0, 0]

    # Log raw vs filtered: use last measured raw if available, else repeat previous
    raw_xs.append(cx if measured else raw_xs[-1] if raw_xs else initial_center)
    filt_xs.append(pred_cx)
    timestamps.append(frame_idx)
    frame_idx += 1

    # Draw YOLO boxes and labels
    for box, conf, cls in zip(
            results.boxes.xyxy.cpu().numpy(),
            results.boxes.conf.cpu().numpy(),
            results.boxes.cls.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)
        label = f"{model.names[int(cls)]} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Control error & pan update
    frame_center = frame.shape[1] / 2.0
    error = pred_cx - frame_center
    pan_delta = Kp * error
    current_pan += pan_delta
    # send_pan_to_servo(current_pan)

    # Visualize predicted center
    cv2.circle(frame, (int(pred_cx), int(frame.shape[0] * 0.95)), 5, (0, 0, 255), -1)

    cv2.imshow('YOLO + Kalman Filter', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()

# --- Plot raw vs filtered x-coordinate ---
plt.figure()
plt.plot(timestamps, raw_xs, label="raw x")
plt.plot(timestamps, filt_xs, label="filtered x")
plt.xlabel("Frame")
plt.ylabel("X position (px)")
plt.title("Raw vs. Filtered X over Time")
plt.legend()
plt.tight_layout()
plt.show()  # or plt.savefig("x_vs_filtered.png", dpi=150)
