import threading
import time
import pyautogui
import numpy as np
from PIL import Image


class ColorDetector:
    def __init__(self):
        self.enabled = False
        self.monitor_region = (0, 0, 50, 50)
        self.target_color = (255, 0, 0)
        self.tolerance = 30
        self.check_interval = 0.5
        
        self.detected_callback = None
        self.check_thread = None
        self.running = False
    
    def set_params(self, enabled=False, x=0, y=0, width=50, height=50,
                   target_color=(255, 0, 0), tolerance=30):
        self.enabled = enabled
        self.monitor_region = (x, y, width, height)
        self.target_color = target_color
        self.tolerance = tolerance
    
    def set_detected_callback(self, callback):
        self.detected_callback = callback
    
    def _color_matches(self, color):
        for c1, c2 in zip(color, self.target_color):
            if abs(c1 - c2) > self.tolerance:
                return False
        return True
    
    def _check_loop(self):
        while self.running:
            if self.enabled:
                x, y, w, h = self.monitor_region
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                
                found = False
                for py in range(h):
                    for px in range(w):
                        pixel = screenshot.getpixel((px, py))
                        if self._color_matches(pixel):
                            found = True
                            break
                    if found:
                        break
                
                if found and self.detected_callback:
                    self.detected_callback((x, y, w, h))
            
            time.sleep(self.check_interval)
    
    def start(self):
        if self.running:
            return
        self.running = True
        self.check_thread = threading.Thread(target=self._check_loop)
        self.check_thread.daemon = True
        self.check_thread.start()
    
    def stop(self):
        self.running = False
        if self.check_thread:
            self.check_thread.join(timeout=1)
    
    def get_current_color(self, x, y):
        screenshot = pyautogui.screenshot()
        return screenshot.getpixel((x, y))
