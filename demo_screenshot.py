import cv2
import numpy as np
from advanced_gesture_detector import AdvancedGestureDetector
import time

def create_demo_screenshots():
    """Tạo screenshots demo cho GitHub README"""
    
    # Khởi tạo detector
    detector = AdvancedGestureDetector()
    cap = cv2.VideoCapture(0)
    
    print("📸 Demo Screenshot Creator")
    print("Hướng dẫn:")
    print("1. Thực hiện cử chỉ trước camera")
    print("2. Nhấn SPACE để chụp screenshot")
    print("3. Nhấn Q để thoát")
    
    screenshot_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Lật frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Phát hiện bàn tay
        results = detector.hands.process(rgb_frame)
        
        gesture = "No hand detected"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Vẽ landmarks
                detector.mp_draw.draw_landmarks(
                    frame, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS)
                
                # Nhận diện cử chỉ
                gesture, finger_states = detector.detect_gesture(hand_landmarks.landmark)
        
        # Vẽ UI đẹp cho demo
        h, w = frame.shape[:2]
        
        # Background gradient
        overlay = np.zeros_like(frame)
        overlay[:100] = [50, 50, 50]  # Dark background
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Title
        cv2.putText(frame, "Advanced Hand Gesture Recognition", 
                   (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Gesture
        cv2.putText(frame, f"Gesture: {gesture}", 
                   (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "Press SPACE to capture demo | Q to quit", 
                   (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Demo Screenshot Creator', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord(' '):  # Space
            screenshot_count += 1
            filename = f"demo_{screenshot_count}.png"
            cv2.imwrite(filename, frame)
            print(f"📸 Saved: {filename}")
            
            # Flash effect
            flash = np.ones_like(frame) * 255
            cv2.addWeighted(flash, 0.5, frame, 0.5, 0, frame)
            cv2.imshow('Demo Screenshot Creator', frame)
            cv2.waitKey(100)
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Created {screenshot_count} demo screenshots")

if __name__ == "__main__":
    create_demo_screenshots()