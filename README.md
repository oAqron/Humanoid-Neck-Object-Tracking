# NTU-Jetson-Gesture-CV-Project
# Gesture-Driven Response System on NVIDIA Jetson

**Real-time human gesture recognition → automated text/audio response**

## Project Overview

We build an end-to-end pipeline that:

1. Captures live camera frames on a Jetson  
2. Runs MediaPipe (or YOLO-Pose) for body/hand keypoints  
3. Feeds a 1D-Conv/LSTM classifier on sequences of keypoints  
4. Maps recognized gestures (“wave” / “dance”) → text or speech output  

---

## Directory Structure

```text
├── data/           # Raw gesture video clips (wave, dance)
├── notebooks/      # EDA & preprocessing demos
├── src/            # Main scripts and modules
├── docs/           # Diagrams, reports
├── environment.yml # Conda environment spec
└── README.md       # Project overview & instructions
