import cv2
import numpy as np
from gesture_detector import GestureDetector

def main():
    # Khởi tạo camera và gesture detector
    cap = cv2.VideoCapture(0)
    detector = GestureDetector()
    
    print("Hand Gesture Recognition Started!")
    print("Gestures to detect:")
    print("- Down-up (upward): Bàn tay hướng lên")
    print("- Up-down (downward): Bàn tay hướng xuống") 
    print("- Right-left (leftward): Bàn tay hướng trái")
    print("- Left-right (rightward): Bàn tay hướng phải")
    print("- Back-forward (forward): Bàn tay xa camera")
    print("- Forward-back (backward): Bàn tay gần camera")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Lật frame theo chiều ngang để có cảm giác như nhìn gương
        frame = cv2.flip(frame, 1)
        
        # Chuyển đổi BGR sang RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Phát hiện bàn tay
        results = detector.hands.process(rgb_frame)
        
        gesture_text = "No hand detected"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Vẽ landmarks lên frame
                detector.mp_draw.draw_landmarks(
                    frame, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS)
                
                # Nhận diện cử chỉ
                gesture_text = detector.detect_gesture(hand_landmarks.landmark)
        
        # Hiển thị kết quả
        cv2.putText(frame, f"Gesture: {gesture_text}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Hiển thị hướng dẫn
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Hand Gesture Recognition', frame)
        
        # Thoát khi nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()