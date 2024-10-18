# hand_tracking.py
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpDrawing = mp.solutions.drawing_utils

    def track_hands(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        return results

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mpDrawing.draw_landmarks(frame, hand_landmarks, self.mphands.HAND_CONNECTIONS)
        return frame
