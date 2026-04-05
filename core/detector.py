import cv2
import numpy as np
import pyautogui
import threading


class ImageDetector:
    def __init__(self):
        self.targets = []
        self.threshold = 0.8
        self.current_target_index = 0
    
    def add_target(self, template_path, name=""):
        try:
            template = cv2.imread(template_path)
            if template is None:
                return False
            self.targets.append({
                "name": name or f"目标{len(self.targets) + 1}",
                "template": template,
                "path": template_path
            })
            return True
        except Exception as e:
            print(f"添加目标失败: {e}")
            return False
    
    def remove_target(self, index):
        if 0 <= index < len(self.targets):
            self.targets.pop(index)
    
    def clear_targets(self):
        self.targets = []
    
    def set_threshold(self, threshold):
        self.threshold = threshold
    
    def capture_target_from_screen(self, region=None):
        if region:
            x, y, w, h = region
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
        else:
            screenshot = pyautogui.screenshot()
        return np.array(screenshot)
    
    def find_target(self, target_index=None):
        if not self.targets:
            return None
        
        idx = target_index if target_index is not None else self.current_target_index
        if idx >= len(self.targets):
            idx = 0
        
        target = self.targets[idx]
        template = target["template"]
        
        screenshot = pyautogui.screenshot()
        screen_array = np.array(screenshot)
        
        screen_gray = cv2.cvtColor(screen_array, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= self.threshold:
            h, w = template_gray.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, target["name"])
        
        return None
    
    def find_all_targets(self):
        found = []
        for i, target in enumerate(self.targets):
            result = self.find_target(i)
            if result:
                found.append(result)
        return found
    
    def next_target(self):
        self.current_target_index = (self.current_target_index + 1) % len(self.targets) if self.targets else 0
        return self.current_target_index
    
    def save_target(self, image_array, name):
        import os
        from pathlib import Path
        
        target_dir = Path("D:/自制连点器/config/targets")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        path = target_dir / f"{name}.png"
        cv2.imwrite(str(path), image_array)
        return str(path)
