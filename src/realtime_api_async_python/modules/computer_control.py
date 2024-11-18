"""
Computer control module for automating keyboard, mouse, and system operations.
Requires the following packages:
- pyautogui
- pytesseract
- pygetwindow
"""

import pyautogui
import pytesseract
import pygetwindow as gw
import subprocess
import os
from typing import Tuple, List, Optional
import logging
from PIL import Image
import time

# Configure PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Add small delay between actions

class ComputerControl:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def type_text(self, text: str, interval: float = 0.1):
        """Type text with a natural delay between keystrokes."""
        pyautogui.write(text, interval=interval)
        
    def press_key(self, key: str):
        """Press a single key."""
        pyautogui.press(key)
        
    def hotkey(self, *keys: str):
        """Press a combination of keys."""
        pyautogui.hotkey(*keys)
        
    def mouse_move(self, x: int, y: int, duration: float = 0.2):
        """Move mouse to absolute coordinates."""
        pyautogui.moveTo(x, y, duration=duration)
        
    def mouse_click(self, button: str = 'left'):
        """Click the mouse."""
        pyautogui.click(button=button)
        
    def mouse_drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.2):
        """Drag mouse from start to end coordinates."""
        pyautogui.moveTo(start_x, start_y, duration=duration/2)
        pyautogui.dragTo(end_x, end_y, duration=duration/2)
        
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen resolution."""
        return pyautogui.size()
        
    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image:
        """Take a screenshot of the entire screen or specified region."""
        return pyautogui.screenshot(region=region)
        
    def find_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
        """Find an image on screen and return its coordinates."""
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            return location
        except pyautogui.ImageNotFoundException:
            return None
            
    def get_text_from_image(self, image: Image) -> str:
        """Extract text from image using OCR."""
        return pytesseract.image_to_string(image)
        
    def get_active_window(self):
        """Get the currently active window."""
        return gw.getActiveWindow()
        
    def get_window_by_title(self, title: str):
        """Find window by title."""
        return gw.getWindowsWithTitle(title)
        
    def focus_window(self, window):
        """Bring window into focus."""
        window.activate()
        
    def move_window(self, window, x: int, y: int):
        """Move window to specified coordinates."""
        window.moveTo(x, y)
        
    def resize_window(self, window, width: int, height: int):
        """Resize window to specified dimensions."""
        window.resizeTo(width, height)
        
    def run_system_command(self, command: str) -> Tuple[str, str, int]:
        """Run a system command and return stdout, stderr, and return code."""
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode

    def wait_for_image(self, image_path: str, timeout: int = 10, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
        """Wait for an image to appear on screen."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = self.find_on_screen(image_path, confidence)
            if location:
                return location
            time.sleep(0.5)
        return None

    def click_image(self, image_path: str, confidence: float = 0.9) -> bool:
        """Find and click on an image."""
        location = self.find_on_screen(image_path, confidence)
        if location:
            self.mouse_move(*location)
            self.mouse_click()
            return True
        return False
