import sys
import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Recognize function to detect hand gestures
def recognize(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Error loading image"
    
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Initialize Mediapipe Hands
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return "No hand detected"

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Normalize landmarks
            landmarks = normalize_landmarks(hand_landmarks.landmark)
            
            # Check for specific gestures
            thumb_up = is_thumb_up(landmarks)
            stop = is_stop(landmarks)
            
            if thumb_up:
                return "thumbs-up"
            elif stop:
                return "stop"

    return "No recognized gesture"

# Function to normalize landmarks
def normalize_landmarks(landmarks):
    landmarks = np.array([(lm.x, lm.y, lm.z) for lm in landmarks])
    center = np.mean(landmarks, axis=0)
    max_dist = np.max(np.linalg.norm(landmarks - center, axis=1))
    return (landmarks - center) / max_dist

# Function to check if the gesture is thumbs-up
def is_thumb_up(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = landmarks[mp_hands.HandLandmark.THUMB_CMC]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    thumb_up_condition = (
        thumb_tip[1] < thumb_ip[1] < thumb_mcp[1] < thumb_cmc[1] and
        thumb_tip[0] < index_tip[0]
    )

    return thumb_up_condition

# Function to check if the gesture is stop
def is_stop(landmarks):
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    
    palm_base = landmarks[mp_hands.HandLandmark.WRIST]

    stop_condition = (
        index_tip[1] < palm_base[1] and
        middle_tip[1] < palm_base[1] and 
        ring_tip[1] < palm_base[1] and 
        pinky_tip[1] < palm_base[1] and
        abs(index_tip[0] - palm_base[0]) < 0.2 and
        abs(middle_tip[0] - palm_base[0]) < 0.2 and
        abs(ring_tip[0] - palm_base[0]) < 0.2 and
        abs(pinky_tip[0] - palm_base[0]) < 0.2
    )

    return stop_condition

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = recognize(image_path)
    print(result)
