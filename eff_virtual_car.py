import math
import cv2
import mediapipe as mp
import os
import socket
import time as t

# ============ ESP32 Socket Setup ============
ESP32_IP = "192.168.137.155"   # change to your ESP32 static IP
ESP32_PORT = 8080

def connect_socket():
    """Try connecting to ESP32 until success"""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((ESP32_IP, ESP32_PORT))
            print("✅ Connected to ESP32")
            return s
        except Exception as e:
            print(f"⚠️ Connection failed: {e}. Retrying in 2s...")
            t.sleep(2)

s = connect_socket()

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Mediapipe Setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

# Webcam input
cap = cv2.VideoCapture(0)

# Track last command
last_command = None
last_send_time = 0

def send_command(cmd):
    """Send command only if changed OR heartbeat expired"""
    global last_command, last_send_time, s
    now = t.time()

    if cmd != last_command or (now - last_send_time > 0.5):
        try:
            s.send((cmd + "\n").encode())
            print(f"➡️ Sent: {cmd}")
            last_command = cmd
            last_send_time = now
        except Exception as e:
            print(f"⚠️ Socket error: {e}, reconnecting...")
            try:
                s.close()
            except:
                pass
            s = connect_socket()

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Process frame with Mediapipe
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        co = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x, normalizedLandmark.y,
                            imageWidth, imageHeight
                        )
                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

        current_cmd = "S"  # default STOP

        # ======== Gesture Logic + Virtual Steering ========
        if len(co) == 2:
            xm, ym = int((co[0][0] + co[1][0]) / 2), int((co[0][1] + co[1][1]) / 2)
            cv2.circle(image, (xm, ym), 120, (195, 255, 62), 4)
            cv2.line(image, tuple(co[0]), tuple(co[1]), (0, 255, 255), 6)

            if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                current_cmd = "L"
                cv2.putText(image, "Turn Left", (50, 50), font, 0.8, (0, 255, 0), 2)
                cv2.arrowedLine(image, (xm, ym), (xm-100, ym), (0, 255, 0), 5)

            elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                current_cmd = "L"
                cv2.putText(image, "Turn Left", (50, 50), font, 0.8, (0, 255, 0), 2)
                cv2.arrowedLine(image, (xm, ym), (xm-100, ym), (0, 255, 0), 5)

            elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                current_cmd = "R"
                cv2.putText(image, "Turn Right", (50, 50), font, 0.8, (0, 255, 0), 2)
                cv2.arrowedLine(image, (xm, ym), (xm+100, ym), (0, 255, 0), 5)

            elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                current_cmd = "R"
                cv2.putText(image, "Turn Right", (50, 50), font, 0.8, (0, 255, 0), 2)
                cv2.arrowedLine(image, (xm, ym), (xm+100, ym), (0, 255, 0), 5)

            else:
                current_cmd = "F"
                cv2.putText(image, "Forward", (50, 50), font, 0.8, (0, 255, 0), 2)
                cv2.arrowedLine(image, (xm, ym), (xm, ym-100), (0, 255, 0), 5)

        elif len(co) == 1:
            current_cmd = "B"
            cv2.putText(image, "Backward", (50, 50), font, 0.8, (0, 0, 255), 2)
            cv2.circle(image, tuple(co[0]), 60, (0, 0, 255), 4)
            cv2.arrowedLine(image, tuple(co[0]), (co[0][0], co[0][1]+100), (0, 0, 255), 5)

        else:
            current_cmd = "S"
            cv2.putText(image, "STOP", (50, 50), font, 0.8, (0, 0, 255), 2)

        # Send command efficiently
        send_command(current_cmd)

        # Show video
        cv2.putText(image, f"Cmd: {current_cmd}", (10, imageHeight-20), font, 0.7, (255,255,0), 2)
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == ord('q'):
            send_command("S")
            break

        t.sleep(0.05)  # throttle ~20 FPS

cap.release()
s.close()
