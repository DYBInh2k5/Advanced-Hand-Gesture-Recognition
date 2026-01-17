import json
import time
import os
from datetime import datetime

class GestureRecorder:
    def __init__(self):
        self.recordings = {}
        self.current_recording = None
        self.recording_name = None
        self.is_recording = False
        self.recordings_dir = "recordings"
        
        # Tạo thư mục recordings nếu chưa có
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)
    
    def start_recording(self, name=None):
        """Bắt đầu ghi cử chỉ"""
        if name is None:
            name = f"gesture_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.recording_name = name
        self.current_recording = {
            'name': name,
            'timestamp': time.time(),
            'gestures': [],
            'duration': 0
        }
        self.is_recording = True
        return f"Started recording: {name}"
    
    def stop_recording(self):
        """Dừng ghi và lưu file"""
        if not self.is_recording or not self.current_recording:
            return "No active recording"
        
        self.current_recording['duration'] = time.time() - self.current_recording['timestamp']
        
        # Lưu vào file
        filename = os.path.join(self.recordings_dir, f"{self.recording_name}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.current_recording, f, indent=2, ensure_ascii=False)
        
        self.recordings[self.recording_name] = self.current_recording
        self.is_recording = False
        
        return f"Recording saved: {filename}"
    
    def add_gesture(self, gesture, landmarks=None):
        """Thêm cử chỉ vào recording hiện tại"""
        if not self.is_recording or not self.current_recording:
            return
        
        gesture_data = {
            'timestamp': time.time() - self.current_recording['timestamp'],
            'gesture': gesture,
            'landmarks': self._serialize_landmarks(landmarks) if landmarks else None
        }
        
        self.current_recording['gestures'].append(gesture_data)
    
    def _serialize_landmarks(self, landmarks):
        """Chuyển landmarks thành format có thể serialize"""
        if not landmarks:
            return None
        
        return [[lm.x, lm.y, lm.z] for lm in landmarks]
    
    def load_recording(self, filename):
        """Tải recording từ file"""
        filepath = os.path.join(self.recordings_dir, filename)
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            recording = json.load(f)
        
        return recording
    
    def list_recordings(self):
        """Liệt kê tất cả recordings"""
        recordings = []
        if os.path.exists(self.recordings_dir):
            for filename in os.listdir(self.recordings_dir):
                if filename.endswith('.json'):
                    recordings.append(filename[:-5])  # Bỏ .json
        return recordings
    
    def play_recording(self, name):
        """Phát lại recording (trả về sequence của gestures)"""
        recording = self.load_recording(f"{name}.json")
        if not recording:
            return None
        
        return recording['gestures']
    
    def get_recording_stats(self, name):
        """Lấy thống kê của recording"""
        recording = self.load_recording(f"{name}.json")
        if not recording:
            return None
        
        gestures = recording['gestures']
        gesture_counts = {}
        
        for gesture_data in gestures:
            gesture = gesture_data['gesture']
            if gesture not in gesture_counts:
                gesture_counts[gesture] = 0
            gesture_counts[gesture] += 1
        
        return {
            'name': recording['name'],
            'duration': recording['duration'],
            'total_gestures': len(gestures),
            'unique_gestures': len(gesture_counts),
            'gesture_breakdown': gesture_counts,
            'gestures_per_second': len(gestures) / recording['duration'] if recording['duration'] > 0 else 0
        }