import numpy as np
import pyautogui
from PIL import Image


def capture_screen(region=None):
    if region:
        x, y, w, h = region
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
    else:
        screenshot = pyautogui.screenshot()
    return np.array(screenshot)


def get_pixel_color(x, y):
    screenshot = pyautogui.screenshot()
    return screenshot.getpixel((x, y))


def get_region_colors(x, y, width, height):
    screenshot = pyautogui.screenshot()
    colors = []
    for cy in range(y, y + height):
        row = []
        for cx in range(x, x + width):
            row.append(screenshot.getpixel((cx, cy)))
        colors.append(row)
    return colors


def color_match(color1, color2, tolerance):
    for c1, c2 in zip(color1, color2):
        if abs(c1 - c2) > tolerance:
            return False
    return True


def find_color_in_region(target_color, x, y, width, height, tolerance=30):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    img_array = np.array(screenshot)
    
    target_color = np.array(target_color)
    
    diff = np.abs(img_array.astype(np.int16) - target_color)
    max_diff = np.max(diff, axis=2) if len(diff.shape) == 3 else np.abs(diff)
    
    matches = np.where(max_diff <= tolerance)
    if len(matches[0]) > 0:
        return (matches[1][0] + x, matches[0][0] + y)
    return None
