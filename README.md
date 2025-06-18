# 🤖 CarryMate: Intelligent Human-Following Robot with Gesture Control

CarryMate is an AI-powered mobile robot designed to autonomously follow a human target using computer vision and hand gesture commands. It leverages YOLOv8 for real-time person detection, ByteTrack for multi-object tracking, and MediaPipe for gesture-based start/stop control.

---

## 🔍 Project Overview

**CarryMate** aims to reduce physical strain in environments where users need to carry multiple or heavy items — such as warehouses, campuses, or delivery zones. By detecting a person from the back and interpreting simple hand gestures, the robot can smartly follow or stop, acting like a "third hand" for logistics or personal use.

Demo: https://youtu.be/nevOTUfiOmk

---

## 🎯 Features

- 🧠 **Human detection and tracking** using YOLOv8 and ByteTrack
- ✋ **Gesture control** with open palm to stop, closed fist to follow
- 📦 **Payload support** for carrying lightweight or moderately heavy items
- 🛞 **2-wheel motion control** via serial commands to a microcontroller
- ⚙️ **Real-time operation** with webcam input (or compatible camera module)
- ⚡ GPU-accelerated with CUDA-enabled PyTorch (if available)

---

## 🚀 System Architecture

1. **Input:** Real-time video from camera
2. **Detection:** YOLOv8 detects humans
3. **Tracking:** ByteTrack assigns consistent IDs
4. **Gesture Recognition:** MediaPipe analyzes hand
5. **Decision Making:** If gesture = "fist", track target ID and move accordingly
6. **Motion Output:** Serial command to robot (e.g., '1' for forward, '3' for left)

---

## 🛠️ Requirements

- Python 3.8+
- PyTorch with CUDA (optional but recommended)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- OpenCV
- MediaPipe

Install dependencies:

```bash
pip install ultralytics opencv-python mediapipe pyserial

