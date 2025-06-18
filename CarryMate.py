import cv2
from ultralytics import YOLO
import mediapipe as mp
import serial
import time
import torch

use_cuda = torch.cuda.is_available()
device = "cuda" if use_cuda else "cpu"
print("Using device:", device)

ser = serial.Serial('COM3', 115200) 
time.sleep(2)  


model = YOLO("yolov8n.pt")
model.to(device)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
follow_mode = False
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

last_command = ""
last_sent_time = 0
min_interval = 0.1  

def detect_gesture(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    return_status = [hand_landmarks.landmark[tip].y > hand_landmarks.landmark[tip - 2].y for tip in finger_tips]

    if all(return_status):
        return "fist"
    elif not any(return_status):
        return "open"
    else:
        return "none"


def get_command(x_center, frame_width):
    center_zone = frame_width // 3
    if x_center < frame_width // 2 - center_zone // 2:
        return "3" 
    elif x_center > frame_width // 2 + center_zone // 2:
        return "2" 
    else:
        return "1"  


def send_command_if_needed(command):
    global last_command, last_sent_time
    now = time.time()
    if command != last_command or (now - last_sent_time) > min_interval:
        ser.write(command.encode())
        print(f"Command: {command}")
        last_command = command
        last_sent_time = now

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_hands = hands.process(img_rgb)


    if result_hands.multi_hand_landmarks:
        for handLms in result_hands.multi_hand_landmarks:
            gesture = detect_gesture(handLms)
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            if gesture == "fist":
                follow_mode = True
                cv2.putText(frame, "Follow ON", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif gesture == "open":
                follow_mode = False
                cv2.putText(frame, "Follow OFF", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    if follow_mode:
        results = model.track(frame, persist=True, classes=0, device=device)[0]  # Person only

        if results.boxes.id is not None:
            ids = results.boxes.id.cpu().numpy()
            boxes = results.boxes.xyxy.cpu().numpy()

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2
                track_id = int(ids[i])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                command = get_command(x_center, W)
                send_command_if_needed(command)
                break
        else:
            send_command_if_needed("0")
    else:
        send_command_if_needed("0")

    cv2.imshow("Robot Follow with Gesture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
