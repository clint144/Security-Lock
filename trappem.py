# face_access_control.py
import json, base64
import numpy as np
import cv2
from deepface import DeepFace
import serial
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "enroll", "face_db.json")
COM_PORT = "COM6"
BAUD_RATE = 9600
GRANT_THRESHOLD = 0.60  # adjust after testing

# helper functions
def b64_to_np(s):
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

# load embedding (ONLY YOU)
with open(DB_PATH, "r") as f:
    raw_db = json.load(f)

# Use the actual key from face_db.json: "clintita"
clint_emb = b64_to_np(raw_db["clintita"]["embedding"])

# set up face detector (OpenCV Haar cascade)
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    raise RuntimeError("Failed to load Haar cascade for face detection.")

print("[SYSTEM] Loaded Haar cascade for face detection.")

# arduino serial
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("[SYSTEM] Arduino Connected.")

def run_face_recognition():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("No camera detected.")

    print("[SYSTEM] Camera opened. Show your face to the camera.")
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # flip so it's like a mirror
        frame = cv2.flip(frame, 1)

        # detect face with OpenCV
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

        if len(faces) == 0:
            # draw info and continue
            cv2.putText(frame, "No face detected", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow("Face Access Control", frame)

            # timeout
            if time.time() - start > 30:
                print("[SYSTEM] No face detected - Access Denied (timeout).")
                ser.write(b"DENIED\n")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[SYSTEM] Quit manual.")
                ser.write(b"DENIED\n")
                break

            continue

        # use the largest detected face
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        face_roi = frame[y:y+h, x:x+w]

        try:
            print("Running DeepFace on cropped face...")
            emb_obj = DeepFace.represent(
                img_path=face_roi,
                model_name="ArcFace",
                detector_backend="skip",   # do NOT run any detector
                enforce_detection=False,   # tolerate low-quality crops
                align=False                # don't try to re-align
            )
            print("DeepFace success")

            emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)

            score = cosine_similarity(emb, clint_emb)
            is_granted = score >= GRANT_THRESHOLD

            label = f"{'Clint' if is_granted else 'Denied'} | sim={score:.2f}"
            color = (0, 255, 0) if is_granted else (0, 0, 255)

            cv2.putText(frame, label, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if is_granted:
                print(f"[SYSTEM] Clint Verified. sim={score:.2f}")
                ser.write(b"APPROVED\n")
                cv2.imshow("Face Access Control", frame)
                cv2.waitKey(2000)
                break

        except Exception as e:
            print("DeepFace error on cropped face:", e)
            cv2.putText(frame, "DeepFace error", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # show frame every loop
        cv2.imshow("Face Access Control", frame)

        if time.time() - start > 30:
            print("[SYSTEM] Timeout - Access Denied.")
            ser.write(b"DENIED\n")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[SYSTEM] Quit manual.")
            ser.write(b"DENIED\n")
            break

    cap.release()
    cv2.destroyAllWindows()

# run immediately
print("[SYSTEM] Ready for Face Scan.")
run_face_recognition()
