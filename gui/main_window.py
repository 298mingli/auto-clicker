import customtkinter as ctk
import threading
import time
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox

from gui.widgets import (
    ClickSettingsPanel, PositionPanel, StopConditionPanel,
    ImageTargetPanel, ColorMonitorPanel, HotkeyPanel
)
from core.clicker import ClickEngine
from core.detector import ImageDetector
from core.color_detector import ColorDetector
from core.hotkey import HotkeyManager
from utils.config import load_config, save_config, export_config, import_config


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("桌面连点器")
        self.geometry("800x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.config = load_config()
        
        self.click_engine = ClickEngine()
        self.image_detector = ImageDetector()
        self.color_detector = ColorDetector()
        self.hotkey_manager = HotkeyManager()
        
        self.mode = "fixed"
        self.image_mode = "single"
        self.capturing = False
        self.coord_thread = None
        self.running = False
        self.tracking_enabled = True
        
        self.setup_ui()
        self.setup_callbacks()
        self.start_coord_tracking()
        self.setup_tray()
        self.bind_keys()
        self.color_detector.start()
    
    def bind_keys(self):
        self.bind("<F8>", lambda e: self.toggle_capture_position())
        self.bind("<F6>", lambda e: self.get_color_at_mouse())
    
    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_basic = self.tabview.add("基础点击")
        self.tab_image = self.tabview.add("图像识别")
        self.tab_color = self.tabview.add("颜色识别")
        self.tab_settings = self.tabview.add("设置")
        
        self.setup_basic_tab()
        self.setup_image_tab()
        self.setup_color_tab()
        self.setup_settings_tab()
        self.setup_control_bar()
    
    def setup_basic_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_basic, label_text="基础点击")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.click_settings = ClickSettingsPanel(scroll)
        self.click_settings.pack(fill="x", padx=5, pady=5)
        
        self.position_panel = PositionPanel(
            scroll, 
            on_capture=self.start_capture_position,
            on_stop_track=self.on_tracking_changed
        )
        self.position_panel.pack(fill="x", padx=5, pady=5)
        
        self.stop_condition = StopConditionPanel(scroll)
        self.stop_condition.pack(fill="x", padx=5, pady=5)
    
    def setup_image_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_image, label_text="图像识别")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.image_target = ImageTargetPanel(
            scroll,
            on_add=self.add_image_target,
            on_remove=self.remove_image_target,
            on_clear=self.clear_image_targets
        )
        self.image_target.pack(fill="x", padx=5, pady=5)
        
        mode_frame = ctk.CTkFrame(scroll)
        mode_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(mode_frame, text="图像模式:").pack(side="left", padx=10)
        self.image_mode_combo = ctk.CTkComboBox(mode_frame, values=["单目标循环", "多目标轮循"], width=150)
        self.image_mode_combo.set("单目标循环")
        self.image_mode_combo.pack(side="left", padx=10)
        
        ctk.CTkButton(scroll, text="截取屏幕区域作为目标", command=self.capture_screen_region).pack(pady=10)
    
    def setup_color_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_color, label_text="颜色识别")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.color_monitor = ColorMonitorPanel(
            scroll,
            on_get_color=self.get_color_at_mouse
        )
        self.color_monitor.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(scroll, text="说明: 当监控区域内检测到目标颜色时触发点击").pack(pady=10)
    
    def setup_settings_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_settings, label_text="设置")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll, text="界面主题", font=("Microsoft YaHei", 14, "bold")).pack(pady=(10, 5))
        
        theme_row = ctk.CTkFrame(scroll)
        theme_row.pack(pady=5)
        ctk.CTkLabel(theme_row, text="主题:").pack(side="left", padx=10)
        self.theme_combo = ctk.CTkComboBox(theme_row, values=["dark", "light", "system"], width=120, command=self.change_theme)
        self.theme_combo.set(self.config.get("theme", "dark"))
        self.theme_combo.pack(side="left", padx=10)
        
        sep1 = ctk.CTkFrame(scroll, height=2, fg_color="gray30")
        sep1.pack(fill="x", padx=10, pady=10)
        
        self.hotkey_panel = HotkeyPanel(scroll, on_apply=self.apply_hotkey_settings)
        self.hotkey_panel.pack(fill="x", padx=5, pady=5)
        
        sep2 = ctk.CTkFrame(scroll, height=2, fg_color="gray30")
        sep2.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(scroll, text="配置管理", font=("Microsoft YaHei", 14, "bold")).pack(pady=(0, 5))
        
        ctk.CTkButton(scroll, text="保存配置", command=self.save_current_config, width=150).pack(pady=5)
        
        btn_frame = ctk.CTkFrame(scroll)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="导出", command=self.export_config, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="导入", command=self.load_exported_config, width=80).pack(side="left", padx=5)
        
        about_label = ctk.CTkLabel(scroll, text="关于", font=("Microsoft YaHei", 14, "bold"))
        about_label.pack(pady=(15, 5))
        
        about_frame = ctk.CTkFrame(scroll)
        about_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(about_frame, text="桌面连点器 v1.0", font=("Microsoft YaHei", 11)).pack(pady=5)
        ctk.CTkLabel(about_frame, text="快捷键: F6-取色 | F8-取坐标 | F9-开始 | F10-停止 | F11-暂停", 
                    font=("Consolas", 9), text_color="gray").pack(pady=2)
        ctk.CTkLabel(about_frame, text="图像识别: 拖动选择区域添加目标", 
                    font=("Consolas", 9), text_color="gray").pack(pady=2)
    
    def setup_control_bar(self):
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.start_btn = ctk.CTkButton(control_frame, text="开始 (F9)", command=self.start_clicking, width=120)
        self.start_btn.pack(side="left", padx=10, pady=10)
        
        self.stop_btn = ctk.CTkButton(control_frame, text="停止 (F10)", command=self.stop_clicking, width=120, state="disabled")
        self.stop_btn.pack(side="left", padx=10, pady=10)
        
        self.pause_btn = ctk.CTkButton(control_frame, text="暂停 (F11)", command=self.pause_clicking, width=120, state="disabled")
        self.pause_btn.pack(side="left", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(control_frame, text="状态: 等待", font=("Consolas", 12))
        self.status_label.pack(side="left", padx=20)
        
        self.click_count_label = ctk.CTkLabel(control_frame, text="点击: 0", font=("Consolas", 12))
        self.click_count_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(control_frame, text="时间: 00:00", font=("Consolas", 12))
        self.time_label.pack(side="left", padx=10)
    
    def setup_callbacks(self):
        self.click_engine.click_callback = self.on_click
        self.click_engine.stop_callback = self.on_stop
        
        self.hotkey_manager.set_callbacks(
            start_cb=self.start_clicking,
            stop_cb=self.stop_clicking,
            pause_cb=self.pause_clicking
        )
        
        self.color_detector.set_detected_callback(self.on_color_detected)
        
        self.hotkey_manager.start()
    
    def start_coord_tracking(self):
        pass
    
    def on_tracking_changed(self, disabled):
        pass
    
    def toggle_capture_position(self):
        if not self.capturing:
            self.capturing = True
            self.status_label.configure(text="状态: 点击获取坐标...")
            self.position_panel.set_button_state("确认 (F8)")
        else:
            self.capturing = False
            self.status_label.configure(text="状态: 等待")
            x, y = pyautogui.position()
            self.position_panel.set_position(x, y)
            self.position_panel.set_button_state("获取坐标 (F8)")
    
    def start_capture_position(self):
        self.capturing = True
        self.status_label.configure(text="状态: 点击获取坐标...")
        
        def wait_click():
            from pynput import mouse
            
            def on_click(x, y, button, pressed):
                if pressed:
                    self.position_panel.set_position(x, y)
                    self.capturing = False
                    self.status_label.configure(text="状态: 等待")
                    return False
            
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()
        
        thread = threading.Thread(target=wait_click, daemon=True)
        thread.start()
    
    def capture_screen_region(self):
        pass
    
    def add_image_target(self):
        self.status_label.configure(text="状态: 拖动选择目标区域...")
        self.after(100, self._start_region_selection)
    
    def _start_region_selection(self):
        def select_region():
            from pynput import mouse
            
            start_pos = None
            
            def on_click(x, y, button, pressed):
                nonlocal start_pos
                if pressed and start_pos is None:
                    start_pos = (x, y)
                elif pressed and start_pos is not None:
                    end_pos = (x, y)
                    listener.stop()
                    
                    x1 = min(start_pos[0], end_pos[0])
                    y1 = min(start_pos[1], end_pos[1])
                    x2 = max(start_pos[0], end_pos[0])
                    y2 = max(start_pos[1], end_pos[1])
                    
                    screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
                    
                    import os
                    from pathlib import Path
                    target_dir = Path("D:/自制连点器/config/targets")
                    target_dir.mkdir(parents=True, exist_ok=True)
                    
                    name = f"target_{len(self.image_detector.targets) + 1}"
                    path = target_dir / f"{name}.png"
                    screenshot.save(str(path))
                    
                    self.image_detector.add_target(str(path), name)
                    self.image_target.add_target_name(name)
                    
                    self.status_label.configure(text="状态: 等待")
            
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()
        
        thread = threading.Thread(target=select_region, daemon=True)
        thread.start()
    
    def remove_image_target(self, idx):
        if 0 <= idx < len(self.image_detector.targets):
            self.image_detector.remove_target(idx)
    
    def clear_image_targets(self):
        self.image_detector.clear_targets()
    
    def get_color_at_mouse(self):
        x, y = pyautogui.position()
        color = pyautogui.screenshot().getpixel((x, y))
        self.color_monitor.set_color(color)
    
    def on_color_detected(self, region):
        if self.running:
            x, y, w, h = region
            self.click_engine._do_click(x + w // 2, y + h // 2)
    
    def on_click(self, count):
        self.click_count_label.configure(text=f"点击: {count}")
    
    def on_stop(self, reason):
        self.status_label.configure(text=f"状态: {reason}")
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.pause_btn.configure(state="disabled")
        self.pause_btn.configure(text="暂停 (F11)")
    
    def start_clicking(self):
        if self.running:
            return
        
        current_tab = self.tabview.get()
        
        if current_tab == "基础点击":
            self.mode = "fixed"
            self._start_fixed_clicking()
        elif current_tab == "图像识别":
            self.mode = "image"
            self.image_mode = self.image_mode_combo.get()
            self._start_image_clicking()
        elif current_tab == "颜色识别":
            self.mode = "color"
            self._start_color_clicking()
    
    def _start_fixed_clicking(self):
        self.running = True
        
        click_type = self.click_settings.get_click_type()
        click_action = self.click_settings.get_click_action()
        interval = self.click_settings.get_interval()
        random_offset = self.click_settings.get_random_offset()
        
        condition, value = self.stop_condition.get_condition()
        
        self.click_engine.set_click_params(
            click_type=click_type,
            click_action=click_action,
            interval=interval,
            random_offset=random_offset,
            stop_condition=condition,
            stop_count=value if condition == "count" else 100,
            stop_time=value if condition == "time" or condition == "color" else 300
        )
        
        x, y = self.position_panel.get_position()
        region = self.position_panel.get_region()
        
        if region:
            self.click_engine.set_position(0, 0, region)
        elif x is not None and y is not None:
            self.click_engine.set_position(x, y)
        
        self.click_engine.start()
        
        self.status_label.configure(text="状态: 运行中 (基础点击)")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.pause_btn.configure(state="normal")
        
        self.update_time()
    
    def _start_image_clicking(self):
        if not self.image_detector.targets:
            from tkinter import messagebox
            messagebox.showwarning("提示", "请先添加图像目标")
            return
        
        self.running = True
        self.click_engine.set_click_params(
            click_type=self.click_settings.get_click_type(),
            click_action=self.click_settings.get_click_action(),
            interval=self.click_settings.get_interval(),
            random_offset=self.click_settings.get_random_offset(),
            stop_condition="none"
        )
        self.image_detector.set_threshold(self.image_target.get_threshold())
        
        thread = threading.Thread(target=self._image_click_loop, daemon=True)
        thread.start()
        
        self.status_label.configure(text="状态: 运行中 (图像识别)")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.pause_btn.configure(state="normal")
    
    def _image_click_loop(self):
        import time
        while self.running and not self.click_engine.paused:
            if self.image_mode == "单目标循环":
                result = self.image_detector.find_target()
            else:
                result = self.image_detector.find_all_targets()
                if result:
                    result = result[0]
            
            if result:
                x, y, name = result
                self.click_engine._do_click(x, y)
                self.click_count_label.configure(text=f"点击: {self.click_engine.click_count}")
            
            time.sleep(self.click_engine.interval)
        
        if self.running:
            self.on_stop("图像识别完成")
    
    def _start_color_clicking(self):
        self.running = True
        
        params = self.color_monitor.get_params()
        self.color_detector.set_params(
            enabled=params["enabled"],
            x=params["x"],
            y=params["y"],
            width=params["width"],
            height=params["height"],
            target_color=params["target_color"],
            tolerance=params["tolerance"]
        )
        
        self.status_label.configure(text="状态: 运行中 (颜色识别)")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.pause_btn.configure(state="normal")
    
    def stop_clicking(self):
        self.click_engine.stop()
    
    def pause_clicking(self):
        paused = self.click_engine.pause()
        if paused:
            self.status_label.configure(text="状态: 已暂停")
            self.pause_btn.configure(text="继续 (F11)")
        else:
            self.status_label.configure(text="状态: 运行中")
            self.pause_btn.configure(text="暂停 (F11)")
    
    def update_time(self):
        if self.running:
            status = self.click_engine.get_status()
            elapsed = int(status.get("elapsed", 0))
            mins, secs = divmod(elapsed, 60)
            self.time_label.configure(text=f"时间: {mins:02d}:{secs:02d}")
            self.after(1000, self.update_time)
    
    def change_theme(self, theme=None):
        if theme is None:
            theme = self.theme_combo.get()
        ctk.set_appearance_mode(theme)
        self.config["theme"] = theme
    
    def save_current_config(self):
        save_config(self.config)
        messagebox.showinfo("提示", "配置已保存")
    
    def export_config(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            export_config(self.config, path)
            messagebox.showinfo("提示", "配置已导出")
    
    def load_exported_config(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.config = import_config(path)
            save_config(self.config)
            messagebox.showinfo("提示", "配置已导入")
    
    def apply_hotkey_settings(self):
        hotkeys = self.hotkey_panel.get_hotkeys()
        self.hotkey_manager.set_hotkeys(
            start=hotkeys["start"],
            stop=hotkeys["stop"],
            pause=hotkeys["pause"]
        )
        self.hotkey_manager.stop()
        self.hotkey_manager.start()
        messagebox.showinfo("提示", f"热键已更新\n开始: {hotkeys['start']}\n停止: {hotkeys['stop']}\n暂停: {hotkeys['pause']}")
    
    def setup_tray(self):
        pass
    
    def on_closing(self):
        self.click_engine.stop()
        self.hotkey_manager.stop()
        self.color_detector.stop()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
