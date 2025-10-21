import cv2
import mediapipe as mp
import math
import socket
import json

# --- Networking Setup ---
UDP_IP = "127.0.0.1"  # Localhost
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start webcam capture
cap = cv2.VideoCapture(0)

# --- State and Threshold Variables ---
PINCH_THRESHOLD = 30
last_sent_message = "" # Prevents sending the same message every frame

print("Starting hand gesture detection. Press 'ESC' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    # Initialize data dictionary
    data = {
        "vertical_position": 50,  # Default middle position
        "is_shooting": False
    }

    if results.multi_hand_landmarks and results.multi_handedness:
        # Tracks your RIGHT hand (labeled 'Left' in the mirrored view)
        if results.multi_handedness[0].classification[0].label == 'Left':
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # --- Pinch Detection ---
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = image.shape
            thumb_px = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_px = (int(index_tip.x * w), int(index_tip.y * h))
            distance = math.hypot(thumb_px[0] - index_px[0], thumb_px[1] - index_px[1])
            
            # Get the wrist y-coordinate for vertical position
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
            
            # Convert to percentage (0% at top, 100% at bottom)
            height_percentage = int(wrist_y * 100)
            height_percentage = max(0, min(100, height_percentage))
            
            # Update data dictionary
            data["vertical_position"] = height_percentage
            
            if distance < PINCH_THRESHOLD:
                data["is_shooting"] = True
                cv2.putText(image, "SHOOTING!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                data["is_shooting"] = False
                
            # Display the percentage on screen
            cv2.putText(image, f"Height: {height_percentage}%", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Visual indicator bar
            bar_height = int((height_percentage / 100) * 300)  # 300 pixels max height
            cv2.rectangle(image, (w - 50, h - 350), (w - 20, h - 50), (100, 100, 100), 2)
            cv2.rectangle(image, (w - 48, h - 50 - bar_height), (w - 22, h - 50), (0, 255, 0), -1)
    else:
        # No hand detected - keep default values
        data["vertical_position"] = 50
        data["is_shooting"] = False

    # --- Send Data Over UDP ---
    # Convert dictionary to JSON string
    json_data = json.dumps(data)
    
    # Send only if the data has changed to avoid flooding
    if json_data != last_sent_message:
        sock.sendto(json_data.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent: {json_data}") # For debugging
        last_sent_message = json_data

    cv2.imshow('Controller', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()