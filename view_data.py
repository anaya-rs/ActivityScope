import sqlite3
from datetime import datetime

class ActivityAnalyzer:
    def __init__(self, db_path='activity_log.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def get_recent_activity(self, limit=10):
        """Get the most recent activity entries"""
        self.cursor.execute('''
            SELECT timestamp, window_title, process_name, mouse_clicks, key_presses, idle_time
            FROM activity_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_process_summary(self):
        """Get summary by process"""
        self.cursor.execute('''
            SELECT process_name, COUNT(*) as entries, 
                   SUM(mouse_clicks) as total_clicks,
                   SUM(key_presses) as total_keys,
                   AVG(idle_time) as avg_idle
            FROM activity_logs 
            GROUP BY process_name
            ORDER BY entries DESC
        ''')
        return self.cursor.fetchall()
    
    def print_summary(self):
        print("=== RECENT ACTIVITY ===")
        recent = self.get_recent_activity()
        for entry in recent:
            timestamp, window, process, clicks, keys, idle = entry
            print(f"{timestamp} | {process} | Clicks: {clicks} | Keys: {keys} | Idle: {idle:.1f}s")
        
        print("\n=== PROCESS SUMMARY ===")
        summary = self.get_process_summary()
        for process, entries, clicks, keys, idle in summary:
            print(f"{process:15} | Entries: {entries:3} | Clicks: {clicks:4} | Keys: {keys:4} | Avg Idle: {idle:.1f}s")

if __name__ == "__main__":
    analyzer = ActivityAnalyzer()
    analyzer.print_summary()
