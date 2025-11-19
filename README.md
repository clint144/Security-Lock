# Security-Lock 🔐  
**Face Recognition–Based Access Control with Arduino**

This project is a **face-recognition security lock system** that only unlocks when it recognizes an authorized user’s face. It combines:

- A Python program using **OpenCV** + **DeepFace** (ArcFace embeddings)  
- An **Arduino Mega 2560** that controls LEDs / lock hardware through **serial commands**

The system demonstrates **real-world biometric authentication** using artificial intelligence and microcontroller feedback.

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

1. Python opens webcam → captures frames  
2. DeepFace (ArcFace) extracts a face embedding  
3. The embedding is compared with the stored authorized embedding  
4. Cosine similarity determines:
   - ✔️ **APPROVED** — face matches  
   - ❌ **DENIED** — face detected but not authorized  
   - ⏳ **NOFACE** — no face detected  
5. Python sends serial messages to the Arduino  
6. Arduino uses an LED to show system status  

---

## 🖥️ System Architecture

### **Python (PC Side)**

- Captures webcam frames  
- Performs face detection + embedding  
- Loads authorized embedding from `face_db.json`  
- Computes cosine similarity  
- Sends messages to Arduino:
  - `"SEARCH"`
  - `"APPROVED"`
  - `"DENIED"`
  - `"NOFACE"`

---

### **Arduino (Microcontroller Side)**

- Listens for serial commands  
- Controls **one LED**  
- Uses blink patterns to display system status  
- (Optional) Supports relay/sensor modules  

---

## 🔌 Hardware

- Arduino Mega 2560  
- Breadboard  
- **One red LED**  
- 220Ω–1kΩ resistor  
- Jumper wires  
- USB cable  
- Webcam  
- (Optional) relay module, HC-SR04 ultrasonic sensor  

---

## 💻 Software & Libraries

### **Python Requirements**

Install dependencies:

```bash
pip install opencv-python deepface numpy pyserial
```

Built-in modules used:

- `json`  
- `base64`  
- `os`  
- `time`  

---

### **Arduino Requirements**

- Arduino IDE  
- Select **Arduino Mega 2560** board  
- Serial Monitor **must be closed** while Python is running  

---

## 📂 Repository Structure

```
Security-Lock/
│
├── README.md
├── trappem.py                # Main Python script
├── face_access_control.py    # Older version (optional)
│
├── enroll/
│   └── face_db.json          # Authorized user’s embedding
│
├── arduino/
│   └── security_lock.ino     # Arduino LED controller
│
├── images/                   # Wiring images (optional)
└── videos/                   # Video links (in README)
```

---

## ⚙️ Setup & Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/clint144/Security-Lock
```

### **2. Install Python Dependencies**

```bash
pip install opencv-python deepface numpy pyserial
```

### **3. Upload Arduino Code**

1. Open `arduino/security_lock.ino`  
2. Select **Arduino Mega 2560**  
3. Upload the sketch  
4. **Close Serial Monitor**  

### **4. Connect LED**

- **Long leg → pin 13**  
- **Short leg → resistor → GND**  

---

## ▶️ How to Run

1. Connect Arduino via USB  
2. Make sure Serial Monitor is CLOSED  
3. Run Python script:

```bash
python trappem.py
```

4. Show your face to the camera  
5. LED indicates the result:

- APPROVED → **solid ON**  
- DENIED → **fast blink**  
- SEARCH → **slow blink**  
- NOFACE → **off**  

---

## 🔴 LED Status Logic

| Condition                   | Serial Message | LED Behavior   |
|----------------------------|----------------|----------------|
| Searching for a face       | `"SEARCH"`     | Slow blinking  |
| Authorized face detected   | `"APPROVED"`   | Solid ON       |
| Unauthorized face detected | `"DENIED"`     | Fast blinking  |
| No face detected (timeout) | `"NOFACE"`     | OFF            |

---

## 🎥 Process / Documentation Videos

### ✔️ Video 1 — Full System Demo  
https://youtube.com/shorts/qk67F_gxURk?si=Ss1e98_KVKMWUg7C

(Add more videos here if needed.)

---

## ⚠️ Known Issues / Limitations

- DeepFace may run slowly on lower-end CPUs  
- Lighting affects accuracy  
- Only one authorized user supported  
- Wrong COM port breaks communication  
- Fast movement can trigger `"NOFACE"`  

---

## 🚀 Future Improvements

- Add OLED screen  
- Add relay-controlled door lock  
- Add multi-user support  
- Add backup fingerprint authentication  
- Convert to Raspberry Pi standalone  
- Encrypt stored embeddings  

---

## 🙌 Credits

- **Clinton Ita** — Developer  
- DeepFace (ArcFace model)  
- OpenCV  
- Arduino Mega 2560  
