import math

class GestureDetection:
    def is_hand_open(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]  # Thumb tip
        index_tip = hand_landmarks.landmark[8]  # Index finger tip
        middle_tip = hand_landmarks.landmark[12]  # Middle finger tip

        thumb_index_distance = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
        thumb_middle_distance = math.sqrt((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2)

        if thumb_index_distance > 0.15 and thumb_middle_distance > 0.15:
            return True  # Open hand
        return False  # Closed hand

    def get_hand_direction(self, hand_landmarks, frame_width):
        wrist = hand_landmarks.landmark[0]  # Wrist point
        wrist_x = wrist.x * frame_width

        if wrist_x < frame_width / 3:
            return "Left"
        elif wrist_x > 2 * frame_width / 3:
            return "Right"
        else:
            return "Center"
