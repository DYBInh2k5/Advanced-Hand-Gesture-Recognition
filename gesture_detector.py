import cv2
import mediapipe as mp
import numpy as np
import math

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def calculate_angle(self, p1, p2, p3):
        """Tính góc giữa 3 điểm"""
        v1 = np.array([p1.x - p2.x, p1.y - p2.y])
        v2 = np.array([p3.x - p2.x, p3.y - p2.y])
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        return np.degrees(angle)
    
    def get_hand_direction(self, landmarks):
        """Xác định hướng của bàn tay"""
        wrist = landmarks[0]
        middle_finger_mcp = landmarks[9]
        
        # Vector từ cổ tay đến khớp giữa ngón giữa
        dx = middle_finger_mcp.x - wrist.x
        dy = middle_finger_mcp.y - wrist.y
        
        # Tính góc
        angle = math.atan2(dy, dx) * 180 / math.pi
        
        # Chuẩn hóa góc về [0, 360)
        if angle < 0:
            angle += 360
            
        return angle
    
    def detect_gesture(self, landmarks):
        """Nhận diện cử chỉ dựa trên landmarks"""
        if not landmarks:
            return "No hand detected"
        
        # Lấy tọa độ các điểm quan trọng
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Tính hướng của bàn tay
        hand_angle = self.get_hand_direction(landmarks)
        
        # Kiểm tra xem các ngón tay có duỗi thẳng không
        fingers_up = []
        
        # Ngón cái
        if thumb_tip.x > landmarks[3].x:  # Thumb is up if tip is to the right of IP joint
            fingers_up.append(1)
        else:
            fingers_up.append(0)
            
        # Các ngón còn lại
        for tip_id in [8, 12, 16, 20]:
            if landmarks[tip_id].y < landmarks[tip_id - 2].y:  # Tip is above PIP joint
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        total_fingers = sum(fingers_up)
        
        # Phân loại cử chỉ dựa trên hướng và số ngón tay duỗi
        if total_fingers == 5:  # Tất cả ngón tay duỗi
            if 45 <= hand_angle <= 135:  # Hướng lên
                return "Down-up (upward)"
            elif 225 <= hand_angle <= 315:  # Hướng xuống
                return "Up-down (downward)"
            elif 315 <= hand_angle or hand_angle <= 45:  # Hướng phải
                return "Left-right (rightward)"
            elif 135 <= hand_angle <= 225:  # Hướng trái
                return "Right-left (leftward)"
        
        # Kiểm tra cử chỉ forward/backward dựa trên kích thước bàn tay
        hand_size = abs(middle_tip.x - wrist.x) + abs(middle_tip.y - wrist.y)
        
        if hand_size > 0.3:  # Bàn tay lớn (gần camera)
            return "Forward-back (backward)"
        elif hand_size < 0.15:  # Bàn tay nhỏ (xa camera)
            return "Back-forward (forward)"
        
        return f"Unknown gesture (fingers: {total_fingers})"