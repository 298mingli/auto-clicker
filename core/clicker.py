import time
import random
import threading
import pyautogui


class ClickEngine:
    def __init__(self):
        self.running = False
        self.paused = False
        self.click_count = 0
        self.total_clicks = 0
        self.start_time = None
        self.stop_reason = None
        
        self.click_type = "left"
        self.click_action = "single"
        self.interval = 1.0
        self.random_offset = 0.2
        self.target_count = 0
        self.stop_condition = "none"
        self.stop_count = 100
        self.stop_time = 300
        
        self.fixed_x = None
        self.fixed_y = None
        self.region = None
        
        self.click_callback = None
        self.stop_callback = None
    
    def set_click_params(self, click_type="left", click_action="single", 
                        interval=1.0, random_offset=0.2, target_count=0,
                        stop_condition="none", stop_count=100, stop_time=300):
        self.click_type = click_type
        self.click_action = click_action
        self.interval = interval
        self.random_offset = random_offset
        self.target_count = target_count
        self.stop_condition = stop_condition
        self.stop_count = stop_count
        self.stop_time = stop_time
    
    def set_position(self, x, y, region=None):
        self.fixed_x = x
        self.fixed_y = y
        self.region = region
    
    def _do_click(self, x, y):
        button_map = {"left": "left", "middle": "middle", "right": "right"}
        button = button_map.get(self.click_type, "left")
        
        if self.click_action == "double":
            pyautogui.click(x, y, button=button, clicks=2, interval=0.05)
        else:
            pyautogui.click(x, y, button=button)
        
        self.click_count += 1
        self.total_clicks += 1
        
        if self.click_callback:
            self.click_callback(self.click_count)
    
    def _get_next_position(self):
        if self.region:
            x = random.randint(self.region[0], self.region[0] + self.region[2])
            y = random.randint(self.region[1], self.region[1] + self.region[3])
            return x, y
        elif self.fixed_x is not None and self.fixed_y is not None:
            offset_x = random.uniform(-self.random_offset * 10, self.random_offset * 10)
            offset_y = random.uniform(-self.random_offset * 10, self.random_offset * 10)
            return self.fixed_x + offset_x, self.fixed_y + offset_y
        return None, None
    
    def _check_stop_condition(self):
        if self.stop_condition == "count" and self.click_count >= self.stop_count:
            self.stop_reason = "达到点击次数"
            return True
        elif self.stop_condition == "time" and self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed >= self.stop_time:
                self.stop_reason = "达到运行时间"
                return True
        return False
    
    def start(self):
        if self.running:
            return
        
        self.running = True
        self.paused = False
        self.click_count = 0
        self.start_time = time.time()
        self.stop_reason = None
        
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()
    
    def _run(self):
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            
            x, y = self._get_next_position()
            if x is not None and y is not None:
                self._do_click(int(x), int(y))
            
            if self._check_stop_condition():
                self.stop()
                break
            
            sleep_time = self.interval + random.uniform(-self.random_offset, self.random_offset)
            sleep_time = max(0.05, sleep_time)
            time.sleep(sleep_time)
    
    def stop(self):
        self.running = False
        if self.stop_callback:
            self.stop_callback(self.stop_reason or "手动停止")
    
    def pause(self):
        self.paused = not self.paused
        return self.paused
    
    def get_status(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            "running": self.running,
            "paused": self.paused,
            "click_count": self.click_count,
            "total_clicks": self.total_clicks,
            "elapsed": elapsed
        }
