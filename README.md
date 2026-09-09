# Desktop Auto Clicker / 桌面连点器

A feature-rich desktop auto clicker with image recognition and color detection, built with Python and CustomTkinter.

一个功能丰富的桌面连点器，支持图像识别和颜色检测，基于 Python + CustomTkinter 构建。

## Features / 功能特性

- **Basic Clicking / 基础点击** — Fixed position or region clicking with configurable interval and click type
- **Image Recognition / 图像识别** — Template matching using OpenCV, auto-click when target image is found on screen
- **Color Detection / 颜色识别** — Monitor a screen region and click when target color is detected
- **Hotkeys / 全局热键** — F6 (color pick), F8 (coordinate pick), F9 (start), F10 (stop), F11 (pause)
- **Config Management / 配置管理** — Save, load, import, and export settings
- **Theme Support / 主题切换** — Dark mode, light mode, and system theme

## Screenshots / 截图

<!-- Add screenshots here if available -->

## Installation / 安装

### Prerequisites / 前置条件

- Python 3.10+
- Windows OS

### Steps / 步骤

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/298mingli/auto-clicker.git
cd auto-clicker

# Install dependencies / 安装依赖
pip install -r requirements.txt

# Run the application / 运行程序
python main.py
```

Or double-click `run.bat` on Windows.

或在 Windows 上双击 `run.bat` 运行。

## Dependencies / 依赖

| Package | Description |
|---------|-------------|
| customtkinter | Modern UI framework |
| pyautogui | Screen automation |
| pynput | Keyboard/mouse listener |
| opencv-python | Image template matching |
| numpy | Array operations |
| Pillow | Image processing |
| pywin32 | Windows API |
| pyinstaller | Build executable |

## Hotkeys / 快捷键

| Key | Action |
|-----|--------|
| F6 | Pick color at mouse position / 获取鼠标位置颜色 |
| F8 | Capture mouse coordinates / 捕获鼠标坐标 |
| F9 | Start clicking / 开始点击 |
| F10 | Stop clicking / 停止点击 |
| F11 | Pause / Resume / 暂停或继续 |

## Usage Modes / 使用模式

### Basic Clicking / 基础点击

Set a fixed position or region, configure click interval, type (left/right/middle), and action (single/double). Supports random offset for natural clicking patterns.

设置固定位置或区域，配置点击间隔、类型（左/右/中键）和动作（单击/双击）。支持随机偏移模拟自然点击。

### Image Recognition / 图像识别

Add target images by dragging to select screen regions. The app will continuously scan for matching images and click when found. Supports single target cycling and multi-target rotation.

通过拖拽选择屏幕区域添加目标图像。程序持续扫描匹配图像并自动点击。支持单目标循环和多目标轮循。

### Color Detection / 颜色识别

Define a monitoring region and target color with tolerance. When the color is detected in the region, the app triggers a click.

定义监控区域和目标颜色（含容差）。当检测到目标颜色时自动触发点击。

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](LICENSE) file for details.

本项目使用 GPL 3.0 协议 — 详情参见 [LICENSE](LICENSE) 文件。

## Contributing / 贡献

Feel free to open issues and pull requests!

欢迎提交 Issue 和 Pull Request！
