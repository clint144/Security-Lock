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
3. Compares embedding to the stored authorized embedding  
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
- Performs face detection + embedding via DeepFace  
- Loads stored embedding from `face_db.json`  
- Computes cosine similarity  
- Sends messages to Arduino:
  - `"SEARCH"`
  - `"APPROVED"`
  - `"DENIED"`
  - `"NOFACE"`

---

### **Arduino (Microcontroller Side)**

- Listens to serial messages  
- Controls **one LED** with different blink patterns  
- (Optional) Can control relay, sensors, locks  

---

## 🔌 Hardware

- Arduino Mega 2560  
- Breadboard  
- **One red LED**  
- Resistor (220Ω–1kΩ)  
- Jumper wires  
- USB cable  
- Webcam  
- (Optional) Relay module, HC-SR04  

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
- Board set to **Arduino Mega 2560**  
- Serial Monitor **must be closed** when Python runs  

---

## 📂 Repository Structure

```
Security-Lock/
│
├── README.md
├── trappem.py                # Main Python script
├── face_access_control.py    # Early version (optional)
│
├── enroll/
│   └── face_db.json          # Stored face embedding
│
├── arduino/
│   └── security_lock.ino     # LED/lock Arduino code
│
├── images/                   # Wiring pictures (optional)
└── videos/                   # Links documented in README
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
3. Upload  
4. CLOSE Serial Monitor  

### **4. Connect LED**

- Long leg → pin **13**  
- Short leg → resistor → **GND**  

---

## ▶️ How to Run

1. Plug in Arduino via USB  
2. Make sure **Serial Monitor is closed**  
3. Run:

```bash
python trappem.py
```

4. Show your face to the camera  
5. LED reacts:

- APPROVED → solid  
- DENIED → fast blink  
- SEARCH → slow blink  
- NOFACE → off  

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

### ✔️ **Video 1 — Full System Demo**

https://youtube.com/shorts/qk67F_gxURk?si=Ss1e98_KVKMWUg7C

(Add more videos here if you upload them later.)

---

## ⚠️ Known Issues / Limitations

- DeepFace can be slow on weak computers  
- Lighting heavily affects detection accuracy  
- Only one authorized user supported right now  
- Wrong COM port breaks serial communication  
- Fast movement may trigger “NOFACE”  

---

## 🚀 Future Improvements

- Add OLED display  
- Add relay to control real lock hardware  
- Support multiple users  
- Add fingerprint/backup authentication  
- Convert to Raspberry Pi standalone  
- Encrypt embedding storage  

---

## 🙌 Credits

- **Clinton Ita** — Developer  
- DeepFace (ArcFace)  
- OpenCV  
- Arduino Mega 2560  
