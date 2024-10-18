import cv2
import pyautogui
from Trackhand import HandTracker
from Detect_Gestures import GestureDetection
import time


tracker = HandTracker()
gesture = GestureDetection()

cap = cv2.VideoCapture(0)


current_hand_state = None
current_direction = None
last_keypress_time = time.time()


cooldown_period = 0.2

while True:
    start_time = time.time()  

    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    results = tracker.track_hands(img)
    img = tracker.draw_landmarks(img, results)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            is_hand_open = gesture.is_hand_open(hand_landmarks)
            hand_direction = gesture.get_hand_direction(hand_landmarks, img.shape[1])

            current_time = time.time()

            if is_hand_open and current_hand_state != "open" and current_time - last_keypress_time > cooldown_period:
                pyautogui.keyDown('w')  
                pyautogui.keyUp('s')  
                current_hand_state = "open"
                last_keypress_time = current_time
            elif not is_hand_open and current_hand_state != "closed" and current_time - last_keypress_time > cooldown_period:
                pyautogui.keyDown('s') 
                pyautogui.keyUp('w') 
                current_hand_state = "closed"
                last_keypress_time = current_time

          
            if hand_direction == "Left" and current_direction != "left" and current_time - last_keypress_time > cooldown_period:
                pyautogui.keyDown('a') 
                pyautogui.keyUp('d')  
                current_direction = "left"
                last_keypress_time = current_time
            elif hand_direction == "Right" and current_direction != "right" and current_time - last_keypress_time > cooldown_period:
                pyautogui.keyDown('d')  
                pyautogui.keyUp('a') 
                current_direction = "right"
                last_keypress_time = current_time
            elif hand_direction == "Center" and current_direction != "center":
              
                pyautogui.keyUp('a')
                pyautogui.keyUp('d')
                current_direction = "center"

           
            hand_state_text = "Hand Open" if is_hand_open else "Hand Closed"
            cv2.putText(img, hand_state_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if is_hand_open else (0, 0, 255), 2)
            cv2.putText(img, hand_direction, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Hand Tracking", img)

    
    elapsed_time = time.time() - start_time
    delay = max(1/60 - elapsed_time, 0) 
    time.sleep(delay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

cv2.destroyAllWindows()


