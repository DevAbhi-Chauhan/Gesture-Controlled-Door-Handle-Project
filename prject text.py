import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands  # type: ignore
mp_drawing = mp.solutions.drawing_utils  # type: ignore

password = "1"
current_input = ""

# Function to determine if the hand is right or left
def determine_left_or_right(hand_landmarks):
    # Get the x-coordinate of the thumb and little finger
    thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    pinky_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    
    if thumb_x < pinky_x:
        return "Right"
    else:
        return "Left"

# Function to determine if the hand is open or closed
def determine_open_or_closed(hand_landmarks):
    # Get the y-coordinate of the index and little fingers
    index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    
    if index_y < pinky_y:
        return 0 # Open hand
    else:
        return 1 # Closed hand

# Initialize the hand tracking module
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0) 

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break
    
    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        hand_type = determine_left_or_right(hand_landmarks)
        hand_open = determine_open_or_closed(hand_landmarks)
        
        # Store the hand gesture as 0 or 1 in a string
        current_input = str(hand_open)
        
        # Check if the string matches the password
        if current_input == password:
            cv2.putText(image, "Door Opened", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            current_input = ""
        else:
            cv2.putText(image, "Please enter password", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(image, hand_type + " hand, " + ("Open" if hand_open == 0 else "Closed"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow('Hand Gesture Recognition', image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
