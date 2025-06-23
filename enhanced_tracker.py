import time
import json
import sqlite3
from datetime import datetime
from pynput import mouse, keyboard
import win32gui
import win32process  # Add this import
import threading
import psutil

class EnhancedActivityTracker:
    def __init__(self):
        self.activity = {
            "mouse_clicks": 0,
            "key_presses": 0,
            "last_input_time": time.time(),
            "active_window": "",
            "active_process": "",
            "category": "Other"
        }
        
        # Define application categories
        self.app_categories = {
            "code.exe": "Development",
            "devenv.exe": "Development", 
            "chrome.exe": "Web Browsing",
            "firefox.exe": "Web Browsing",
            "msedge.exe": "Web Browsing",
            "notepad.exe": "Text Editing",
            "notepad++.exe": "Text Editing",
            "slack.exe": "Communication",
            "teams.exe": "Communication",
            "outlook.exe": "Email",
            "explorer.exe": "File Management",
            "cmd.exe": "Terminal",
            "powershell.exe": "Terminal",
            "windowsterminal.exe": "Terminal"
        }
        
        self.setup_database()
        
    def setup_database(self):
        """Initialize enhanced SQLite database"""
        self.conn = sqlite3.connect('enhanced_activity_log.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                window_title TEXT,
                process_name TEXT,
                category TEXT,
                mouse_clicks INTEGER,
                key_presses INTEGER,
                idle_time REAL,
                is_active BOOLEAN
            )
        ''')
        self.conn.commit()

    def categorize_activity(self, process_name):
        """Categorize activity based on process name"""
        return self.app_categories.get(process_name.lower(), "Other")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.activity["mouse_clicks"] += 1
            self.activity["last_input_time"] = time.time()

    def on_press(self, key):
        self.activity["key_presses"] += 1
        self.activity["last_input_time"] = time.time()

    def get_active_window(self):
        """Get the currently active window title and process - FIXED VERSION"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            
            # Fix: Use win32process.GetWindowThreadProcessId instead of win32gui
            thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name()
            return window_title, process_name
        except Exception as e:
            print(f"Error getting window info: {e}")
            return "Unknown", "Unknown"

    def log_activity(self):
        window_title, process_name = self.get_active_window()
        category = self.categorize_activity(process_name)
        
        self.activity["active_window"] = window_title
        self.activity["active_process"] = process_name
        self.activity["category"] = category
        
        idle_time = time.time() - self.activity["last_input_time"]
        is_active = idle_time < 30  # Consider active if idle < 30 seconds
        timestamp = datetime.now().isoformat()
        
        # Log to database
        self.cursor.execute('''
            INSERT INTO activity_logs 
            (timestamp, window_title, process_name, category, mouse_clicks, key_presses, idle_time, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, window_title, process_name, category,
              self.activity["mouse_clicks"], self.activity["key_presses"], idle_time, is_active))
        self.conn.commit()
        
        # Enhanced logging with categories
        status = "ACTIVE" if is_active else "IDLE"
        log_line = f"{timestamp} | {status} | Category: {category} | App: {process_name} | Window: {window_title[:30]} | Mouse: {self.activity['mouse_clicks']} | Keys: {self.activity['key_presses']} | Idle: {idle_time:.1f}s\n"
        
        with open("enhanced_usage_log.txt", "a", encoding='utf-8') as f:
            f.write(log_line)
        
        # Print to console for real-time feedback
        print(f"{status} | {category:12} | {process_name:15} | Mouse: {self.activity['mouse_clicks']:2} | Keys: {self.activity['key_presses']:2} | Idle: {idle_time:.1f}s")
        
        # Reset counters
        self.activity["mouse_clicks"] = 0
        self.activity["key_presses"] = 0

    def monitor_loop(self):
        while True:
            self.log_activity()
            time.sleep(1)

    def start_tracking(self):
        print("Starting Enhanced Activity Tracker...")
        print("Categories:", list(set(self.app_categories.values())))
        print("Press Ctrl+C to stop")
        print("\nReal-time Activity:")
        print("-" * 80)
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping Enhanced Activity Tracker...")
            mouse_listener.stop()
            keyboard_listener.stop()
            self.conn.close()

if __name__ == "__main__":
    tracker = EnhancedActivityTracker()
    tracker.start_tracking()
