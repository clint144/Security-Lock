# Security-Lock 🔐  
**Face Recognition–Based Access Control with Arduino**

This project is a **face-recognition security lock system** that only unlocks when it recognizes an authorized user’s face. It combines:

- A Python program using **OpenCV** + **DeepFace** (ArcFace embeddings)  
- An **Arduino Mega 2560** that controls LEDs / lock hardware through serial commands  

The system demonstrates real-world biometric authentication using artificial intelligence and microcontroller feedback.

---

## 📚 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Hardware](#-hardware)
- [Software & Libraries](#-software--libraries)
- [Repository Structure](#-repository-structure)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [LED Status Logic](#-led-status-logic)
- [Process / Documentation Videos](#-process--documentation-videos)
- [Known Issues / Limitations](#-known-issues--limitations)
- [Future Improvements](#-future-improvements)
- [Credits](#-credits)

---

## 🧠 Project Overview

The **Security-Lock** system uses a webcam and a stored facial embedding to determine whether access should be granted.

### High-level process:

1. Python opens the webcam and captures frames  
2. DeepFace (ArcFace) extracts a face embedding  
3. The embedding is compared to the stored authorized embedding  
4. Cosine similarity determines:
   - ✔️ **APPROVED** — face matches  
   - ❌ **DENIED** — face detected but not authorized  
   - ⏳ **NOFACE** — no face detected (timeout)  
5. Python sends a serial message (`APPROVED`, `DENIED`, `SEARCH`, `NOFACE`) to the Arduino  
6. Arduino uses an LED to communicate system status  

---

## 🖥️ System Architecture

### Python (PC Side)

- Captures webcam frames  
- Performs face detection + embedding with DeepFace  
- Loads stored authorized face embedding from `face_db.json`  
- Computes cosine similarity  
- Sends serial messages:
  - `"SEARCH"`  
  - `"APPROVED"`  
  - `"DENIED"`  
  - `"NOFACE"`  

### Arduino (Microcontroller Side)

- Listens over serial  
- Controls a single LED  
- Displays system status using blink patterns  
- Can also control relay/motor hardware (optional)

---

## 🔌 Hardware

- Arduino Mega 2560  
- Breadboard  
- One red LED (final version)  
- 220Ω–1kΩ resistor  
- Jumper wires  
- USB cable  
- Webcam  
- (Optional) Relay or HC-SR04 sensor  

---

## 💻 Software & Libraries

### Python Requirements

Install with:

```bash
pip install opencv-python deepface numpy pyserial
