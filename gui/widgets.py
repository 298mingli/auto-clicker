import customtkinter as ctk
import tkinter as tk


class ClickSettingsPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="点击设置", font=("Microsoft YaHei", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        ctk.CTkLabel(self, text="点击类型:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.click_type_combo = ctk.CTkComboBox(self, values=["左键", "中键", "右键"], width=100)
        self.click_type_combo.set("左键")
        self.click_type_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="点击方式:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.click_action_combo = ctk.CTkComboBox(self, values=["单击", "双击"], width=100)
        self.click_action_combo.set("单击")
        self.click_action_combo.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="间隔时间(秒):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.interval_entry = ctk.CTkEntry(self, width=100)
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="随机偏移:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.random_offset_entry = ctk.CTkEntry(self, width=100)
        self.random_offset_entry.insert(0, "0.2")
        self.random_offset_entry.grid(row=4, column=1, padx=10, pady=5)
    
    def get_click_type(self):
        types = {"左键": "left", "中键": "middle", "右键": "right"}
        return types.get(self.click_type_combo.get(), "left")
    
    def get_click_action(self):
        actions = {"单击": "single", "双击": "double"}
        return actions.get(self.click_action_combo.get(), "single")
    
    def get_interval(self):
        try:
            return float(self.interval_entry.get())
        except:
            return 1.0
    
    def get_random_offset(self):
        try:
            return float(self.random_offset_entry.get())
        except:
            return 0.2


class PositionPanel(ctk.CTkFrame):
    def __init__(self, master, on_capture=None, on_stop_track=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_capture = on_capture
        self.on_stop_track = on_stop_track
        
        ctk.CTkLabel(self, text="点击位置", font=("Microsoft YaHei", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        ctk.CTkLabel(self, text="X坐标:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.x_entry = ctk.CTkEntry(self, width=100)
        self.x_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="Y坐标:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.y_entry = ctk.CTkEntry(self, width=100)
        self.y_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.capture_btn = ctk.CTkButton(self, text="获取坐标 (F8)", command=self.start_capture, width=200)
        self.capture_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(self, text="区域模式").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.region_var = ctk.CTkCheckBox(self, text="启用区域随机点击", command=self.toggle_region)
        self.region_var.grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="区域宽:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.region_w = ctk.CTkEntry(self, width=80)
        self.region_w.insert(0, "100")
        self.region_w.grid(row=5, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="区域高:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.region_h = ctk.CTkEntry(self, width=80)
        self.region_h.insert(0, "100")
        self.region_h.grid(row=6, column=1, padx=10, pady=5)
        
        self.region_inputs = [self.region_w, self.region_h]
        for entry in self.region_inputs:
            entry.configure(state="disabled")
    
    def start_capture(self):
        if self.on_capture:
            self.on_capture()
    
    def set_button_state(self, text):
        self.capture_btn.configure(text=text)
    
    def capture_position(self):
        if self.on_capture:
            self.on_capture()
    
    def toggle_region(self):
        state = "normal" if self.region_var.get() else "disabled"
        for entry in self.region_inputs:
            entry.configure(state=state)
    
    def get_position(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            return x, y
        except:
            return None, None
    
    def get_region(self):
        if self.region_var.get():
            try:
                x, y = self.get_position()
                w = int(self.region_w.get())
                h = int(self.region_h.get())
                return (x, y, w, h)
            except:
                return None
        return None
    
    def set_position(self, x, y):
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))


class StopConditionPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="停止条件", font=("Microsoft YaHei", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        ctk.CTkLabel(self, text="条件类型:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.condition_combo = ctk.CTkComboBox(self, values=["无限制", "点击次数", "运行时间"], width=120)
        self.condition_combo.set("无限制")
        self.condition_combo.grid(row=1, column=1, padx=10, pady=5)
        self.condition_combo.bind("<<ComboboxSelected>>", self.toggle_inputs)
        
        ctk.CTkLabel(self, text="点击次数:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.count_entry = ctk.CTkEntry(self, width=100)
        self.count_entry.insert(0, "100")
        self.count_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="运行时间(秒):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.time_entry = ctk.CTkEntry(self, width=100)
        self.time_entry.insert(0, "300")
        self.time_entry.grid(row=3, column=1, padx=10, pady=5)
        
        for widget in [self.count_entry, self.time_entry]:
            widget.configure(state="disabled")
    
    def toggle_inputs(self, event=None):
        condition = self.condition_combo.get()
        if condition == "点击次数":
            self.count_entry.configure(state="normal")
            self.time_entry.configure(state="disabled")
        elif condition == "运行时间":
            self.count_entry.configure(state="disabled")
            self.time_entry.configure(state="normal")
        else:
            self.count_entry.configure(state="disabled")
            self.time_entry.configure(state="disabled")
    
    def get_condition(self):
        condition = self.condition_combo.get()
        if condition == "点击次数":
            return "count", int(self.count_entry.get()) if self.count_entry.cget("state") == "normal" else 0
        elif condition == "运行时间":
            return "time", int(self.time_entry.get()) if self.time_entry.cget("state") == "normal" else 0
        return "none", 0


class ImageTargetPanel(ctk.CTkFrame):
    def __init__(self, master, on_add=None, on_remove=None, on_clear=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_add = on_add
        self.on_remove = on_remove
        self.on_clear = on_clear
        self.target_names = []
        
        ctk.CTkLabel(self, text="图像识别目标", font=("Microsoft YaHei", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        self.target_listbox = tk.Listbox(self, height=4, width=30)
        self.target_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ctk.CTkButton(btn_frame, text="添加", command=self.add_target, width=60).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="删除", command=self.remove_target, width=60).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="清空", command=self.clear_targets, width=60).pack(side="left", padx=5)
        
        ctk.CTkLabel(self, text="灵敏度:").grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
        self.threshold_slider = ctk.CTkSlider(self, from_=0.5, to=1.0, number_of_steps=50)
        self.threshold_slider.set(0.8)
        self.threshold_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        self.threshold_label = ctk.CTkLabel(self, text="0.80")
        self.threshold_label.grid(row=4, column=0, columnspan=2)
        self.threshold_slider.configure(command=self.update_threshold)
    
    def update_threshold(self, value):
        self.threshold_label.configure(text=f"{value:.2f}")
    
    def add_target(self):
        if self.on_add:
            self.on_add()
    
    def remove_target(self):
        selection = self.target_listbox.curselection()
        if selection:
            idx = selection[0]
            self.target_listbox.delete(idx)
            if idx < len(self.target_names):
                self.target_names.pop(idx)
            if self.on_remove:
                self.on_remove(idx)
    
    def clear_targets(self):
        self.target_listbox.delete(0, tk.END)
        self.target_names = []
        if self.on_clear:
            self.on_clear()
    
    def add_target_name(self, name):
        self.target_names.append(name)
        self.target_listbox.insert(tk.END, name)
    
    def get_threshold(self):
        return self.threshold_slider.get()
    
    def get_target_count(self):
        return len(self.target_names)


class ColorMonitorPanel(ctk.CTkFrame):
    def __init__(self, master, on_get_color=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_get_color = on_get_color
        self.current_color = (255, 0, 0)
        
        ctk.CTkLabel(self, text="颜色识别监控", font=("Microsoft YaHei", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        self.enable_var = ctk.CTkCheckBox(self, text="启用颜色识别")
        self.enable_var.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(self, text="监控区域X:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.x_entry = ctk.CTkEntry(self, width=80)
        self.x_entry.insert(0, "0")
        self.x_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="监控区域Y:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.y_entry = ctk.CTkEntry(self, width=80)
        self.y_entry.insert(0, "0")
        self.y_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="区域宽度:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.w_entry = ctk.CTkEntry(self, width=80)
        self.w_entry.insert(0, "50")
        self.w_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="区域高度:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.h_entry = ctk.CTkEntry(self, width=80)
        self.h_entry.insert(0, "50")
        self.h_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ctk.CTkButton(self, text="获取当前颜色 (F6)", command=self.get_current_color, width=150).grid(
            row=6, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(self, text="目标颜色:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.color_label = ctk.CTkLabel(self, text="RGB(255,0,0)", text_color="red")
        self.color_label.grid(row=7, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="容差:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.tolerance_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100)
        self.tolerance_slider.set(30)
        self.tolerance_slider.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
    
    def get_current_color(self):
        if self.on_get_color:
            self.on_get_color()
    
    def set_color(self, color):
        self.current_color = color
        r, g, b = color
        self.color_label.configure(text=f"RGB({r},{g},{b})")
        r_hex = min(255, r + 50)
        self.color_label.configure(text_color=f"#{r:02x}{g:02x}{b:02x}")
    
    def get_params(self):
        return {
            "enabled": self.enable_var.get() == 1,
            "x": int(self.x_entry.get()),
            "y": int(self.y_entry.get()),
            "width": int(self.w_entry.get()),
            "height": int(self.h_entry.get()),
            "target_color": self.current_color,
            "tolerance": int(self.tolerance_slider.get())
        }


class HotkeyPanel(ctk.CTkFrame):
    def __init__(self, master, on_apply=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_apply = on_apply
        
        ctk.CTkLabel(self, text="热键设置", font=("Microsoft YaHei", 14, "bold")).pack(pady=(10, 5))
        
        row1 = ctk.CTkFrame(self)
        row1.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row1, text="开始:", width=60).pack(side="left")
        self.start_key = ctk.CTkEntry(row1, width=100)
        self.start_key.insert(0, "F9")
        self.start_key.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(self)
        row2.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row2, text="停止:", width=60).pack(side="left")
        self.stop_key = ctk.CTkEntry(row2, width=100)
        self.stop_key.insert(0, "F10")
        self.stop_key.pack(side="left", padx=5)
        
        row3 = ctk.CTkFrame(self)
        row3.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row3, text="暂停:", width=60).pack(side="left")
        self.pause_key = ctk.CTkEntry(row3, width=100)
        self.pause_key.insert(0, "F11")
        self.pause_key.pack(side="left", padx=5)
        
        ctk.CTkButton(self, text="应用热键", command=self.apply_hotkeys, width=120).pack(pady=10)
    
    def apply_hotkeys(self):
        if self.on_apply:
            self.on_apply()
    
    def get_hotkeys(self):
        return {
            "start": self.start_key.get(),
            "stop": self.stop_key.get(),
            "pause": self.pause_key.get()
        }
