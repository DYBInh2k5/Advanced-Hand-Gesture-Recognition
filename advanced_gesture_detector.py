import cv2
import mediapipe as mp
import numpy as np
import math
import time
from collections import deque
import json

class AdvancedGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # Hỗ trợ 2 tay
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Lịch sử cử chỉ để phát hiện gesture động
        self.gesture_history = deque(maxlen=10)
        self.last_gesture_time = time.time()
        
        # Thống kê
        self.gesture_count = {}
        self.session_start = time.time()
        
        # Cử chỉ phức tạp
        self.complex_gestures = {
            'wave': [],
            'circle': [],
            'swipe_left': [],
            'swipe_right': []
        }
        
    def get_finger_states(self, landmarks):
        """Trả về trạng thái của từng ngón tay (0=gập, 1=duỗi)"""
        finger_states = []
        
        # Ngón cái - so sánh x coordinate
        if landmarks[4].x > landmarks[3].x:
            finger_states.append(1)
        else:
            finger_states.append(0)
            
        # Các ngón còn lại - so sánh y coordinate
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                finger_states.append(1)
            else:
                finger_states.append(0)
                
        return finger_states
    
    def detect_number_gesture(self, finger_states):
        """Nhận diện số từ 0-5 dựa trên ngón tay"""
        count = sum(finger_states)
        
        # Các trường hợp đặc biệt
        if finger_states == [0, 0, 0, 0, 0]:
            return "Number: 0 (Fist)"
        elif finger_states == [0, 1, 0, 0, 0]:
            return "Number: 1 (Index)"
        elif finger_states == [0, 1, 1, 0, 0]:
            return "Number: 2 (Peace)"
        elif finger_states == [0, 1, 1, 1, 0]:
            return "Number: 3"
        elif finger_states == [0, 1, 1, 1, 1]:
            return "Number: 4"
        elif finger_states == [1, 1, 1, 1, 1]:
            return "Number: 5 (Open hand)"
        elif finger_states == [1, 0, 0, 0, 0]:
            return "Thumbs up"
        elif finger_states == [1, 0, 0, 0, 1]:
            return "Rock and roll 🤟"
        elif finger_states == [0, 1, 0, 0, 1]:
            return "I love you ❤️"
        
        return f"Custom gesture ({count} fingers)"
    
    def detect_hand_shape(self, landmarks):
        """Phát hiện hình dạng bàn tay"""
        # Tính khoảng cách giữa các điểm
        thumb_index_dist = self.calculate_distance(landmarks[4], landmarks[8])
        thumb_middle_dist = self.calculate_distance(landmarks[4], landmarks[12])
        index_middle_dist = self.calculate_distance(landmarks[8], landmarks[12])
        
        # Phát hiện OK gesture
        if thumb_index_dist < 0.05:
            return "OK gesture 👌"
        
        # Phát hiện pointing
        finger_states = self.get_finger_states(landmarks)
        if finger_states == [0, 1, 0, 0, 0]:
            return "Pointing 👉"
            
        return None
    
    def calculate_distance(self, p1, p2):
        """Tính khoảng cách Euclidean giữa 2 điểm"""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def detect_motion_gesture(self, landmarks):
        """Phát hiện cử chỉ chuyển động"""
        if len(self.gesture_history) < 5:
            return None
            
        # Lấy vị trí ngón trỏ trong 5 frame gần nhất
        recent_positions = []
        for hist in list(self.gesture_history)[-5:]:
            if hist and len(hist) > 8:
                recent_positions.append((hist[8].x, hist[8].y))
        
        if len(recent_positions) < 5:
            return None
            
        # Tính vector chuyển động
        start_pos = recent_positions[0]
        end_pos = recent_positions[-1]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Kiểm tra chuyển động đáng kể
        movement_threshold = 0.1
        if abs(dx) > movement_threshold or abs(dy) > movement_threshold:
            if abs(dx) > abs(dy):
                if dx > 0:
                    return "Swipe Right ➡️"
                else:
                    return "Swipe Left ⬅️"
            else:
                if dy > 0:
                    return "Swipe Down ⬇️"
                else:
                    return "Swipe Up ⬆️"
        
        return None
    
    def detect_gesture(self, landmarks):
        """Nhận diện cử chỉ tổng hợp"""
        if not landmarks:
            return "No hand detected", None
        
        # Thêm vào lịch sử
        self.gesture_history.append(landmarks)
        
        # Lấy trạng thái ngón tay
        finger_states = self.get_finger_states(landmarks)
        
        # Kiểm tra các loại cử chỉ
        number_gesture = self.detect_number_gesture(finger_states)
        shape_gesture = self.detect_hand_shape(landmarks)
        motion_gesture = self.detect_motion_gesture(landmarks)
        
        # Ưu tiên hiển thị
        if shape_gesture:
            gesture = shape_gesture
        elif motion_gesture:
            gesture = motion_gesture
        else:
            gesture = number_gesture
        
        # Cập nhật thống kê
        if gesture not in self.gesture_count:
            self.gesture_count[gesture] = 0
        self.gesture_count[gesture] += 1
        
        return gesture, finger_states
    
    def get_statistics(self):
        """Lấy thống kê session"""
        session_time = time.time() - self.session_start
        total_gestures = sum(self.gesture_count.values())
        
        stats = {
            'session_time': session_time,
            'total_gestures': total_gestures,
            'gestures_per_minute': (total_gestures / session_time) * 60 if session_time > 0 else 0,
            'most_common': max(self.gesture_count.items(), key=lambda x: x[1]) if self.gesture_count else ("None", 0)
        }
        
        return stats