# Hand-Gesture-Recognition-System
A real-time hand gesture recognition system using MediaPipe and OpenCV to detect hand landmarks and classify common gestures through webcam input.
# 🖐️ Hand Gesture Recognition

Real-time hand gesture detection using **MediaPipe** and **OpenCV**

---

## 📌 Overview

This project implements a real-time **hand gesture recognition system** using a webcam. It detects hand landmarks and classifies common gestures such as **Fist, Open Hand, Peace, Thumbs Up**, and more.

The system uses:

* MediaPipe for hand tracking
* OpenCV for video processing and visualization

---

## 🚀 Features

* Real-time hand detection
* Finger state detection (up/down)
* Gesture classification
* Visual feedback with labels and colored markers
* Supports multiple hands

---

## 🧠 How It Works

1. Capture video from webcam
2. Detect hand landmarks (21 key points)
3. Determine which fingers are extended
4. Classify gesture using rule-based logic
5. Display results on screen

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hand-gesture-recognition.git
cd hand-gesture-recognition
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python mediapipe
```

---

## ▶️ Usage

Run the program:

```bash
python hand_gesture_recognition.py
```

* Press **Q** to exit
* Show your hand to the camera
* Perform gestures to see detection

---

## ✋ Supported Gestures

* ✊ Fist
* ✋ Open Hand
* ☝️ Pointing
* ✌️ Peace / Victory
* 👍 Thumbs Up
* 🤙 Shaka / Hang Loose
* 🤘 Horns
* And more...

---

## ⚠️ Limitations

* Works best with good lighting
* Thumb detection may vary with hand orientation
* Limited to predefined gestures
* May struggle with overlapping fingers

---

## 🔮 Future Improvements

* Add machine learning-based gesture classification
* Improve left/right hand detection
* Support dynamic gestures (motion-based)
* Integrate with applications (e.g., virtual mouse, games)

---

## 📄 License

This project is open-source and free to use for educational purposes.

---

## 🙌 Acknowledgements

* MediaPipe (Google)
* OpenCV

---

## 📬 Contact

For questions or suggestions, feel free to reach out or open an issue.

---
