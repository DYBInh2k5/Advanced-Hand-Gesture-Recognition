import cv2
import numpy as np
import json
import os
from datetime import datetime
from advanced_gesture_detector import AdvancedGestureDetector

class GestureTrainer:
    def __init__(self):
        self.detector = AdvancedGestureDetector()
        self.training_data = {}
        self.current_gesture_name = None
        self.samples_collected = 0
        self.target_samples = 50
        
        # Tạo thư mục training data
        self.data_dir = "training_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def start_training_session(self, gesture_name):
        """Bắt đầu session training cho một cử chỉ"""
        self.current_gesture_name = gesture_name
        self.samples_collected = 0
        
        if gesture_name not in self.training_data:
            self.training_data[gesture_name] = []
        
        return f"Training session started for: {gesture_name}"
    
    def collect_sample(self, landmarks):
        """Thu thập sample cho cử chỉ hiện tại"""
        if not self.current_gesture_name or not landmarks:
            return False
        
        # Chuẩn hóa landmarks (relative to wrist)
        wrist = landmarks[0]
        normalized_landmarks = []
        
        for lm in landmarks:
            normalized_landmarks.append([
                lm.x - wrist.x,
                lm.y - wrist.y,
                lm.z - wrist.z
            ])
        
        sample = {
            'landmarks': normalized_landmarks,
            'timestamp': datetime.now().isoformat(),
            'gesture': self.current_gesture_name
        }
        
        self.training_data[self.current_gesture_name].append(sample)
        self.samples_collected += 1
        
        return True
    
    def save_training_data(self):
        """Lưu training data vào file"""
        filename = os.path.join(self.data_dir, f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.training_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_progress(self):
        """Lấy tiến độ training hiện tại"""
        if not self.current_gesture_name:
            return None
        
        return {
            'gesture': self.current_gesture_name,
            'collected': self.samples_collected,
            'target': self.target_samples,
            'progress': (self.samples_collected / self.target_samples) * 100
        }
    
    def run_training_interface(self):
        """Giao diện training tương tác"""
        cap = cv2.VideoCapture(0)
        
        gestures_to_train = [
            "thumbs_up", "thumbs_down", "peace", "ok", "fist", 
            "point", "wave", "stop", "rock", "love"
        ]
        
        current_gesture_idx = 0
        collecting = False
        
        print("🎯 Gesture Training Mode")
        print("Instructions:")
        print("- Press SPACE to start/stop collecting samples")
        print("- Press N for next gesture")
        print("- Press S to save data")
        print("- Press Q to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Phát hiện bàn tay
            results = self.detector.hands.process(rgb_frame)
            
            # Vẽ UI
            h, w = frame.shape[:2]
            
            # Background
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (w-10, 120), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Thông tin gesture hiện tại
            current_gesture = gestures_to_train[current_gesture_idx]
            cv2.putText(frame, f"Training: {current_gesture}", 
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Trạng thái collecting
            status = "COLLECTING" if collecting else "READY"
            color = (0, 255, 255) if collecting else (255, 255, 255)
            cv2.putText(frame, f"Status: {status}", 
                       (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Progress
            if self.current_gesture_name == current_gesture:
                progress = self.get_progress()
                if progress:
                    cv2.putText(frame, f"Progress: {progress['collected']}/{progress['target']} ({progress['progress']:.1f}%)", 
                               (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Vẽ landmarks và collect samples
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.detector.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.detector.mp_hands.HAND_CONNECTIONS)
                    
                    # Collect sample nếu đang trong chế độ collecting
                    if collecting and self.current_gesture_name:
                        if self.collect_sample(hand_landmarks.landmark):
                            # Hiển thị feedback
                            cv2.circle(frame, (50, 50), 20, (0, 255, 0), -1)
            
            # Controls
            controls = [
                "SPACE: Start/Stop collecting",
                "N: Next gesture", 
                "S: Save data",
                "Q: Quit"
            ]
            
            for i, control in enumerate(controls):
                cv2.putText(frame, control, 
                           (20, h-100 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            cv2.imshow('Gesture Training', frame)
            
            # Xử lý phím
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord(' '):  # Space
                if collecting:
                    collecting = False
                    print(f"Stopped collecting for {current_gesture}")
                else:
                    self.start_training_session(current_gesture)
                    collecting = True
                    print(f"Started collecting for {current_gesture}")
            elif key == ord('n') or key == ord('N'):
                current_gesture_idx = (current_gesture_idx + 1) % len(gestures_to_train)
                collecting = False
                print(f"Switched to {gestures_to_train[current_gesture_idx]}")
            elif key == ord('s') or key == ord('S'):
                filename = self.save_training_data()
                print(f"Training data saved to: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    trainer = GestureTrainer()
    trainer.run_training_interface()