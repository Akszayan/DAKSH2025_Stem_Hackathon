# 🚗 AR-Based Virtual Steering Car using ESP32

> **Daksh 2025 – STEM Hackathon | SASTRA Deemed University, Thanjavur**
> 🥉 **Third Prize Winner**

---

## 📌 Overview

This project is an **Augmented Reality (AR)–inspired virtual steering control system** for a robotic car, developed as part of the **STEM Hackathon under Daksh 2025** at **SASTRA Deemed University, Thanjavur**.

The system enables **hands-free, gesture-based vehicle control** using a webcam and computer vision. Hand movements are interpreted in real time and transmitted wirelessly to an **ESP32-controlled car**, allowing intuitive steering without physical controllers.

⚠️ **Note:** This is a **general / basic prototype** built within hackathon constraints, intended to demonstrate concept feasibility and learning outcomes rather than production readiness.

---

## 🏆 Hackathon Achievement

* **Event:** Daksh 2025 – STEM Hackathon
* **Institution:** SASTRA Deemed University, Thanjavur
* **Category:** STEM Innovation
* **Result:** 🥉 **Third Prize**

---

## 🎯 Problem Statement

Traditional remote-controlled vehicles rely on:

* Physical controllers
* Joysticks or mobile apps
* Limited accessibility and learning value

This project explores how **computer vision and AR-style interaction** can provide a **more natural and intuitive control interface**, especially for education and human–machine interaction research.

---

## 🧠 Solution Approach

The system uses:

* **Hand gesture detection** via a standard webcam
* **Virtual steering logic** based on relative hand positions
* **Wireless TCP socket communication** to send commands to an ESP32
* **On-board ESP32 firmware** to interpret commands and drive motors safely

Gestures are mapped to motion commands such as:

* Forward (`F`)
* Backward (`B`)
* Left (`L`)
* Right (`R`)
* Stop (`S`)

All commands are transmitted in real time over Wi-Fi and executed by the ESP32 motor controller.

---

## 🏗️ System Architecture

```
Webcam
   ↓
MediaPipe Hands (Gesture Detection)
   ↓
Gesture Logic & Virtual Steering (Python)
   ↓
TCP Socket (Wi-Fi)
   ↓
ESP32 TCP Server (Arduino Firmware)
   ↓
PWM Motor Control (ENA / ENB)
   ↓
Motor Driver → Robotic Car
```

---

## ⚙️ Technologies Used

### Software

* Python
* OpenCV
* MediaPipe (Hands)
* Socket Programming (TCP/IP)

### Firmware

* Arduino (ESP32)
* Wi-Fi (TCP Server)
* PWM Motor Control (LEDC)
* Watchdog Safety Logic

### Hardware

* ESP32 (Wi-Fi enabled microcontroller)
* Motor driver module (L298N / equivalent)
* DC motors / robotic car chassis
* Webcam

---

## ✋ Gesture Mapping (High-Level)

| Hand Detection         | Action     |
| ---------------------- | ---------- |
| Two hands centered     | Forward    |
| Two hands angled left  | Turn Left  |
| Two hands angled right | Turn Right |
| Single hand            | Backward   |
| No hand detected       | Stop       |

The system also implements:

* Command throttling
* Heartbeat-based socket updates
* Automatic reconnection to ESP32

---

## 🔌 ESP32 Firmware Highlights

The ESP32 runs a dedicated **TCP server** that:

* Uses a **static IP** for reliable connectivity
* Accepts real-time motion commands (`F, B, L, R, S`)
* Controls motor speed using **hardware PWM (LEDC)**
* Implements a **watchdog timeout** to stop the car if commands are lost
* Automatically reconnects to Wi-Fi on disconnection

This ensures safe and responsive operation during gesture-based control.

---

## 🧪 Key Learning Outcomes

This project helped us gain hands-on experience in:

* Real-time computer vision pipelines
* Gesture-based human–machine interfaces
* MediaPipe landmark processing
* Wi-Fi socket communication with embedded systems
* ESP32-based robotics control
* Designing intuitive control logic from noisy sensor data

---

## 🌍 Applications & Use Cases

* STEM education demonstrations
* Introductory robotics labs
* Human–computer interaction (HCI) experiments
* Assistive and touchless control systems
* AR/VR-inspired control research

---

## 🧪 Key Learning Outcomes

This project helped us gain hands-on experience in:

* Real-time computer vision pipelines
* Gesture-based human–machine interfaces
* MediaPipe landmark processing
* TCP/IP socket communication
* ESP32 firmware development
* PWM motor control & safety watchdogs
* Designing intuitive control logic from noisy sensor data

---

## 🚧 Limitations

* Webcam-based tracking only (no depth sensing)
* Lighting and background sensitivity
* Hardcoded thresholds for gesture logic
* No obstacle detection or feedback loop

These limitations were acceptable given the hackathon’s scope and time constraints.

---

## 🔮 Future Improvements

* Depth-aware gesture recognition
* IMU or sensor fusion
* Smoother steering using angle regression
* Mobile camera / AR headset integration
* Closed-loop control with feedback

---

## 📜 License

This project is released for **academic, educational, and experimental use**.

---

> *Built as a hands-on STEM innovation during Daksh 2025, combining vision, robotics, and real-time systems.*
