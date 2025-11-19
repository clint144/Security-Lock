# Security-Lock 🔐  
**Face Recognition–Based Access Control with Arduino**

This project is a **face-recognition security lock system** that only “unlocks” when it recognizes an authorized user’s face. It combines:

- A **Python** program using `OpenCV` + `DeepFace` (ArcFace embeddings)  
- An **Arduino Mega 2560** that controls LEDs / lock hardware over **serial**  

The system is designed as a prototype for **contactless, AI-powered access control** that could be used for a door lock, cabinet, or other secure enclosure.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [System Architecture](#system-architecture)  
- [Hardware](#hardware)  
- [Software & Libraries](#software--libraries)  
- [Repository Structure](#repository-structure)  
- [Setup & Installation](#setup--installation)  
- [How to Run](#how-to-run)  
- [LED Status Logic](#led-status-logic)  
- [Process / Documentation Videos](#process--documentation-videos)  
- [Known Issues / Limitations](#known-issues--limitations)  
- [Future Improvements](#future-improvements)  
- [Credits](#credits)

---

## Project Overview

The **Security-Lock** project uses a webcam and a pre-enrolled face embedding to decide whether to grant or deny access.  

**High-level flow:**

1. Python opens the **webcam**, captures frames, and uses **DeepFace (ArcFace model)** to generate face embeddings.
2. It compares the live embedding to a **stored embedding** of the authorized user (me).
3. It computes a **cosine similarity score**:
   - If the score is above a threshold → user is **verified**.
   - If a face is detected but score is too low → **access denied**.
   - If no face is detected for a while → **timeout / no face**.
4. Python sends a status over **serial (USB)** to the Arduino Mega (e.g. `"SEARCH"`, `"APPROVED"`, `"DENIED"`, `"NOFACE"`).
5. The Arduino uses **LED patterns** (and optionally a relay) to show the status of the lock.

This demonstrates **real-world biometric authentication** with live feedback on a microcontroller.

---

## System Architecture

**PC (Python side)**  
- Captures frames from webcam (OpenCV)  
- Uses DeepFace `ArcFace` to embed faces  
- Loads stored authorized embedding from `face_db.json`  
- Computes cosine similarity and decides:
  - APPROVED (my face)
  - DENIED (someone else’s face)
  - NOFACE (timeout / nothing detected)
- Sends serial messages to Arduino:  
  - `"SEARCH"` – when scanning starts  
  - `"APPROVED"` – when authorized face verified  
  - `"DENIED"` – face detected but not authorized  
  - `"NOFACE"` – timeout / no valid face found  

**Arduino (Microcontroller side)**  
- Listens on serial (e.g., `COM6`, 9600 baud)  
- Drives **one red LED** (and optionally other hardware like relay / ultrasonic sensor)  
- Interprets serial commands and sets LED:

See [LED Status Logic](#led-status-logic) for details.

---

## Hardware

- **Elegoo / Arduino Mega 2560**
- **Breadboard**
- **Red LED** (main indicator in final version)
- Resistor(s) for current limiting (e.g., 220Ω–1kΩ)
- Jumper wires
- **USB cable** for PC ↔ Arduino
- (Optional / Earlier versions)
  - Ultrasonic sensor (HC-SR04)
  - Relay module
  - Additional LEDs (blue, green)

---

## Software & Libraries

**On PC (Python):**

- Python 3.11 (or similar)
- `opencv-python`
- `deepface`
- `numpy`
- `pyserial`
- `json`, `base64`, `time`, `os`

Install with:

```bash
pip install opencv-python deepface numpy pyserial
