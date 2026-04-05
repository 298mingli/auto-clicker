import threading
from pynput import keyboard


class HotkeyManager:
    def __init__(self):
        self.start_key = "f9"
        self.stop_key = "f10"
        self.pause_key = "f11"
        
        self.start_callback = None
        self.stop_callback = None
        self.pause_callback = None
        
        self.listener = None
        self.running = False
    
    def set_hotkeys(self, start=None, stop=None, pause=None):
        if start:
            self.start_key = start.lower() if isinstance(start, str) else start
        if stop:
            self.stop_key = stop.lower() if isinstance(stop, str) else stop
        if pause:
            self.pause_key = pause.lower() if isinstance(pause, str) else pause
    
    def set_callbacks(self, start_cb=None, stop_cb=None, pause_cb=None):
        self.start_callback = start_cb
        self.stop_callback = stop_cb
        self.pause_callback = pause_cb
    
    def _normalize_key(self, key):
        key_str = str(key).replace("Key.", "").lower()
        return key_str
    
    def _on_press(self, key):
        try:
            key_str = self._normalize_key(key)
            
            if key_str == self._normalize_key(self.start_key):
                if self.start_callback:
                    self.start_callback()
            elif key_str == self._normalize_key(self.stop_key):
                if self.stop_callback:
                    self.stop_callback()
            elif key_str == self._normalize_key(self.pause_key):
                if self.pause_callback:
                    self.pause_callback()
        except Exception as e:
            print(f"热键错误: {e}")
    
    def start(self):
        if self.running:
            return
        
        self.running = True
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.daemon = True
        self.listener.start()
    
    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def is_running(self):
        return self.running
