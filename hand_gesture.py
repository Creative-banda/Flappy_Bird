import cv2
import mediapipe as mp
import socket
import json
import datetime
import os

# --- Networking Setup ---
UDP_IP = "127.0.0.1"  # Localhost

# Create UDP socket for listening to CAPTURE messages from Godot
listener_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listener_sock.bind((UDP_IP, 5005))  # Python listens on port 5005
listener_sock.settimeout(0.01)  # Non-blocking with short timeout

# Godot address for sending hand position data
godot_address = (UDP_IP, 5006)  # Send to Godot on port 5006

# Create UDP socket for sending data to Godot
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Create a Capture Folder in C: if doesn't exist
if not os.path.exists("C:/Captures"):
    os.makedirs("C:/Captures")


# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Start webcam capture
cap = cv2.VideoCapture(0)

# --- State Variables ---
last_sent_message = "" # Prevents sending the same message every frame

print("Starting LEFT HAND position tracking with Godot communication. Press 'ESC' to quit.")
print("- Tracks LEFT HAND horizontal and vertical position")
print("- Sends position data to Godot on port 5006")
print("- Listens for CAPTURE messages from Godot on port 5005")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # --- Check for incoming UDP commands from Godot ---
    try:
        message_data, addr = listener_sock.recvfrom(1024)
        response = json.loads(message_data.decode())
        
        if response.get("message") == "CAPTURE":
            # Create C:/Captures directory if it doesn't exist
            capture_dir = "C:/Captures"
            if not os.path.exists(capture_dir):
                os.makedirs(capture_dir)
            
            # Generate timestamp for filename (YYYY_MM_DD_HHMM format)
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
            filename = f"{capture_dir}/capture_{timestamp}.png"
            
            # Save the current frame
            cv2.imwrite(filename, image)
            print(f"Screenshot saved: {filename}")
            
            # Show capture feedback on screen
            cv2.putText(image, "SCREENSHOT CAPTURED!", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
    except socket.timeout:
        # No message received, continue normally
        pass
    except json.JSONDecodeError:
        # Invalid JSON received, ignore
        pass
    
    # Process hand detection
    hand_results = hands.process(image_rgb)
    
    # Initialize data dictionary
    data = {
        "horizontal_position": 10,  # Default middle position (0-100)
        "vertical_position": 50     # Default middle position (0-100)
    }

    h, w, _ = image.shape
    left_hand_detected = False
    
    # Check if we can detect the LEFT HAND
    if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
        # Make sure we're tracking the LEFT hand only
        if hand_results.multi_handedness[0].classification[0].label == 'Left':
            hand_landmarks = hand_results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            left_hand_detected = True
            
            # Get wrist position (landmark 0 is the wrist)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            
            # Convert to percentages (0-100)
            horizontal_pos = int(wrist.x * 100)
            vertical_pos = int(wrist.y * 100)  # Direct mapping: hand down = higher value
            
            # Clamp values to 0-100 range
            data["horizontal_position"] = max(0, min(100, horizontal_pos))
            data["vertical_position"] = max(0, min(100, vertical_pos))
            
            # Draw wrist position indicator
            wrist_px = (int(wrist.x * w), int(wrist.y * h))
            cv2.circle(image, wrist_px, 15, (0, 255, 0), -1)  # Green circle
            cv2.putText(image, "WRIST", (wrist_px[0] - 25, wrist_px[1] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Display position info
            cv2.putText(image, f"Horizontal: {data['horizontal_position']}%", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(image, f"Vertical: {data['vertical_position']}%", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "LEFT HAND DETECTED", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # Visual feedback when no hand detected
    if not left_hand_detected:
        cv2.putText(image, "NO LEFT HAND DETECTED", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # --- Send Data Over UDP to Godot ---
    # Only send data when left hand is actually detected
    if left_hand_detected:
        json_data = json.dumps(data)
        
        # Send only if the data has changed to avoid flooding
        if json_data != last_sent_message:
            send_sock.sendto(json_data.encode(), godot_address)
            last_sent_message = json_data

    cv2.imshow('Hand Position Tracker', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()