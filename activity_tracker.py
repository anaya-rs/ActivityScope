import time
import json
import sqlite3
from datetime import datetime
from pynput import mouse, keyboard
import win32gui
import threading
import psutil

class ActivityTracker:
    def __init__(self):
        self.activity = {
            "mouse_clicks": 0,
            "key_presses": 0,
            "last_input_time": time.time(),
            "active_window": "",
            "active_process": "",
        }
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database for storing activity data"""
        self.conn = sqlite3.connect('activity_log.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                window_title TEXT,
                process_name TEXT,
                mouse_clicks INTEGER,
                key_presses INTEGER,
                idle_time REAL
            )
        ''')
        self.conn.commit()

    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed:
            self.activity["mouse_clicks"] += 1
            self.activity["last_input_time"] = time.time()

    def on_press(self, key):
        """Handle keyboard press events"""
        self.activity["key_presses"] += 1
        self.activity["last_input_time"] = time.time()

    def get_active_window(self):
        """Get the currently active window title and process"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32gui.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name()
            return window_title, process_name
        except:
            return "Unknown", "Unknown"

    def log_activity(self):
        """Log current activity to database and file"""
        window_title, process_name = self.get_active_window()
        self.activity["active_window"] = window_title
        self.activity["active_process"] = process_name
        
        idle_time = time.time() - self.activity["last_input_time"]
        timestamp = datetime.now().isoformat()
        
        # Log to database
        self.cursor.execute('''
            INSERT INTO activity_logs 
            (timestamp, window_title, process_name, mouse_clicks, key_presses, idle_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, window_title, process_name, 
              self.activity["mouse_clicks"], self.activity["key_presses"], idle_time))
        self.conn.commit()
        
        # Log to text file for easy viewing
        log_line = f"{timestamp} | Window: {window_title[:50]} | Process: {process_name} | Mouse: {self.activity['mouse_clicks']} | Keys: {self.activity['key_presses']} | Idle: {idle_time:.1f}s\n"
        with open("usage_log.txt", "a", encoding='utf-8') as f:
            f.write(log_line)
        
        # Reset counters
        self.activity["mouse_clicks"] = 0
        self.activity["key_presses"] = 0

    def monitor_loop(self):
        """Main monitoring loop"""
        while True:
            self.log_activity()
            time.sleep(1)  # Log every second

    def start_tracking(self):
        """Start the activity tracking"""
        print("Starting Activity Tracker...")
        print("Press Ctrl+C to stop")
        
        # Start mouse and keyboard listeners
        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping Activity Tracker...")
            mouse_listener.stop()
            keyboard_listener.stop()
            self.conn.close()

if __name__ == "__main__":
    tracker = ActivityTracker()
    tracker.start_tracking()
