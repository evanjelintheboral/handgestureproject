# 🖐️ Hand Gesture Control System

A computer vision project that allows users to control mouse actions using hand gestures through a webcam.

---

## 🚀 Features

- 🖱️ Move mouse cursor using index finger
- 👆 Click using finger pinch gesture
- 🔼 Scroll up using 2 fingers
- 🔽 Scroll down using 3 fingers
- 📸 Take screenshot using closed fist gesture
- 📷 Real-time webcam hand tracking

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Math & Time modules

---

## 📌 How It Works

The system uses **MediaPipe Hand Tracking** to detect hand landmarks from webcam video. Based on finger positions:

- Cursor movement → Index finger position
- Click → Distance between thumb & index finger
- Scroll → Number of fingers raised
- Screenshot → Closed fist detection

---

