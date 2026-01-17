import cv2
import numpy as np
import time
from advanced_gesture_detector import AdvancedGestureDetector
from gesture_controller import GestureController
from gesture_recorder import GestureRecorder

class AdvancedGestureApp:
    def __init__(self):
        self.detector = AdvancedGestureDetector()
        self.controller = GestureController()
        self.recorder = GestureRecorder()
        
        # UI settings
        self.show_landmarks = True
        self.show_stats = True
        self.show_controls = True
        
        # Colors
        self.colors = {
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255),
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
    def draw_ui(self, frame, gesture, finger_states, action_result=None):
        """Vẽ giao diện người dùng"""
        h, w = frame.shape[:2]
        
        # Background cho thông tin
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (w-10, 150), self.colors['black'], -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Hiển thị cử chỉ chính
        cv2.putText(frame, f"Gesture: {gesture}", 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['green'], 2)
        
        # Hiển thị trạng thái ngón tay
        if finger_states:
            finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            finger_text = " | ".join([f"{name}: {'✓' if state else '✗'}" 
                                    for name, state in zip(finger_names, finger_states)])
            cv2.putText(frame, finger_text, 
                       (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['yellow'], 1)
        
        # Hiển thị kết quả hành động
        if action_result:
            cv2.putText(frame, f"Action: {action_result}", 
                       (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['blue'], 2)
        
        # Hiển thị trạng thái
        status_text = []
        if self.controller.enabled:
            status_text.append("Control: ON")
        if self.recorder.is_recording:
            status_text.append(f"Recording: {self.recorder.recording_name}")
        
        if status_text:
            cv2.putText(frame, " | ".join(status_text), 
                       (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['red'], 2)
        
        # Hiển thị thống kê
        if self.show_stats:
            self.draw_statistics(frame)
        
        # Hiển thị controls
        if self.show_controls:
            self.draw_controls(frame)
    
    def draw_statistics(self, frame):
        """Vẽ thống kê"""
        stats = self.detector.get_statistics()
        h, w = frame.shape[:2]
        
        # Background cho stats
        overlay = frame.copy()
        cv2.rectangle(overlay, (w-300, 10), (w-10, 120), self.colors['black'], -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Thống kê
        cv2.putText(frame, f"Session: {stats['session_time']:.1f}s", 
                   (w-290, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)
        cv2.putText(frame, f"Total: {stats['total_gestures']}", 
                   (w-290, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)
        cv2.putText(frame, f"Rate: {stats['gestures_per_minute']:.1f}/min", 
                   (w-290, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)
        cv2.putText(frame, f"Most: {stats['most_common'][0][:15]}", 
                   (w-290, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)
    
    def draw_controls(self, frame):
        """Vẽ hướng dẫn điều khiển"""
        h, w = frame.shape[:2]
        
        controls = [
            "Controls:",
            "C - Toggle Control",
            "R - Start/Stop Recording", 
            "L - Toggle Landmarks",
            "S - Toggle Stats",
            "H - Toggle Help",
            "Q - Quit"
        ]
        
        # Background
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, h-200), (250, h-10), self.colors['black'], -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        for i, control in enumerate(controls):
            color = self.colors['yellow'] if i == 0 else self.colors['white']
            cv2.putText(frame, control, 
                       (20, h-180 + i*25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def handle_keyboard(self, key):
        """Xử lý phím bấm"""
        if key == ord('c') or key == ord('C'):
            if self.controller.enabled:
                self.controller.disable_control()
                return "Control disabled"
            else:
                self.controller.enable_control()
                return "Control enabled"
        
        elif key == ord('r') or key == ord('R'):
            if self.recorder.is_recording:
                return self.recorder.stop_recording()
            else:
                return self.recorder.start_recording()
        
        elif key == ord('l') or key == ord('L'):
            self.show_landmarks = not self.show_landmarks
            return f"Landmarks: {'ON' if self.show_landmarks else 'OFF'}"
        
        elif key == ord('s') or key == ord('S'):
            self.show_stats = not self.show_stats
            return f"Stats: {'ON' if self.show_stats else 'OFF'}"
        
        elif key == ord('h') or key == ord('H'):
            self.show_controls = not self.show_controls
            return f"Help: {'ON' if self.show_controls else 'OFF'}"
        
        return None
    
    def run(self):
        """Chạy ứng dụng chính"""
        cap = cv2.VideoCapture(0)
        
        print("🚀 Advanced Hand Gesture Recognition Started!")
        print("📋 Features:")
        print("   - Number recognition (0-5)")
        print("   - Special gestures (OK, Peace, Rock, etc.)")
        print("   - Motion detection (Swipe, Wave)")
        print("   - Computer control")
        print("   - Gesture recording")
        print("   - Real-time statistics")
        print("\n⌨️  Press 'H' to toggle help")
        
        action_result = None
        last_action_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Lật frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Phát hiện bàn tay
            results = self.detector.hands.process(rgb_frame)
            
            gesture = "No hand detected"
            finger_states = None
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Vẽ landmarks
                    if self.show_landmarks:
                        self.detector.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.detector.mp_hands.HAND_CONNECTIONS)
                    
                    # Nhận diện cử chỉ
                    gesture, finger_states = self.detector.detect_gesture(hand_landmarks.landmark)
                    
                    # Thêm vào recording
                    if self.recorder.is_recording:
                        self.recorder.add_gesture(gesture, hand_landmarks.landmark)
                    
                    # Thực hiện hành động điều khiển
                    if self.controller.enabled:
                        current_time = time.time()
                        if current_time - last_action_time > 2.0:  # Cooldown 2 giây
                            result = self.controller.execute_gesture_action(gesture)
                            if result:
                                action_result = result
                                last_action_time = current_time
            
            # Vẽ UI
            self.draw_ui(frame, gesture, finger_states, action_result)
            
            # Hiển thị frame
            cv2.imshow('Advanced Hand Gesture Recognition', frame)
            
            # Xử lý phím bấm
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
            
            keyboard_result = self.handle_keyboard(key)
            if keyboard_result:
                print(f"📢 {keyboard_result}")
                action_result = keyboard_result
        
        # Dọn dẹp
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Hiển thị thống kê cuối session
        final_stats = self.detector.get_statistics()
        print(f"\n📊 Session Summary:")
        print(f"   Duration: {final_stats['session_time']:.1f} seconds")
        print(f"   Total gestures: {final_stats['total_gestures']}")
        print(f"   Most common: {final_stats['most_common'][0]}")

if __name__ == "__main__":
    app = AdvancedGestureApp()
    app.run()