import pyautogui
import time
import threading
from collections import deque

class GestureController:
    def __init__(self):
        self.enabled = False
        self.last_action_time = time.time()
        self.action_cooldown = 1.0  # 1 giây giữa các hành động
        
        # Vô hiệu hóa fail-safe của pyautogui
        pyautogui.FAILSAFE = False
        
        # Lịch sử để tránh spam
        self.gesture_history = deque(maxlen=5)
        
    def enable_control(self):
        """Bật điều khiển máy tính"""
        self.enabled = True
        
    def disable_control(self):
        """Tắt điều khiển máy tính"""
        self.enabled = False
        
    def can_perform_action(self):
        """Kiểm tra có thể thực hiện hành động không"""
        current_time = time.time()
        if current_time - self.last_action_time > self.action_cooldown:
            self.last_action_time = current_time
            return True
        return False
        
    def execute_gesture_action(self, gesture):
        """Thực hiện hành động dựa trên cử chỉ"""
        if not self.enabled or not self.can_perform_action():
            return False
            
        try:
            # Điều khiển âm lượng
            if "Thumbs up" in gesture:
                pyautogui.press('volumeup')
                return "Volume Up 🔊"
                
            elif "Number: 0" in gesture:
                pyautogui.press('volumedown')
                return "Volume Down 🔉"
                
            # Điều khiển media
            elif "Number: 1" in gesture:
                pyautogui.press('playpause')
                return "Play/Pause ⏯️"
                
            elif "Swipe Right" in gesture:
                pyautogui.press('nexttrack')
                return "Next Track ⏭️"
                
            elif "Swipe Left" in gesture:
                pyautogui.press('prevtrack')
                return "Previous Track ⏮️"
                
            # Điều khiển trình duyệt
            elif "Number: 2" in gesture:
                pyautogui.hotkey('ctrl', 't')
                return "New Tab 🆕"
                
            elif "Number: 3" in gesture:
                pyautogui.hotkey('ctrl', 'w')
                return "Close Tab ❌"
                
            # Điều khiển cửa sổ
            elif "Number: 4" in gesture:
                pyautogui.hotkey('alt', 'tab')
                return "Switch Window 🔄"
                
            elif "Number: 5" in gesture:
                pyautogui.hotkey('win', 'd')
                return "Show Desktop 🖥️"
                
            # Scroll
            elif "Swipe Up" in gesture:
                pyautogui.scroll(3)
                return "Scroll Up ⬆️"
                
            elif "Swipe Down" in gesture:
                pyautogui.scroll(-3)
                return "Scroll Down ⬇️"
                
            # Screenshot
            elif "OK gesture" in gesture:
                pyautogui.hotkey('win', 'shift', 's')
                return "Screenshot 📸"
                
        except Exception as e:
            print(f"Error executing gesture action: {e}")
            return False
            
        return False