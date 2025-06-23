import sqlite3
from datetime import datetime

class ActivityAnalyzer:
    def __init__(self, db_path='enhanced_activity_log.db'):  # Changed from activity_log.db
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def get_recent_activity(self, limit=10):
        """Get the most recent activity entries"""
        self.cursor.execute('''
            SELECT timestamp, window_title, process_name, category, mouse_clicks, key_presses, idle_time
            FROM activity_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_process_summary(self):
        """Get summary by process"""
        self.cursor.execute('''
            SELECT process_name, category, COUNT(*) as entries, 
                   SUM(mouse_clicks) as total_clicks,
                   SUM(key_presses) as total_keys,
                   AVG(idle_time) as avg_idle
            FROM activity_logs 
            GROUP BY process_name, category
            ORDER BY entries DESC
        ''')
        return self.cursor.fetchall()
    
    def get_category_summary(self):
        """Get summary by category"""
        self.cursor.execute('''
            SELECT category, COUNT(*) as entries, 
                   SUM(mouse_clicks) as total_clicks,
                   SUM(key_presses) as total_keys,
                   AVG(idle_time) as avg_idle
            FROM activity_logs 
            GROUP BY category
            ORDER BY entries DESC
        ''')
        return self.cursor.fetchall()
    
    def print_summary(self):
        print("=== RECENT ACTIVITY ===")
        recent = self.get_recent_activity()
        for entry in recent:
            timestamp, window, process, category, clicks, keys, idle = entry
            print(f"{timestamp} | {category:12} | {process:15} | Clicks: {clicks} | Keys: {keys} | Idle: {idle:.1f}s")
        
        print("\n=== PROCESS SUMMARY ===")
        summary = self.get_process_summary()
        for process, category, entries, clicks, keys, idle in summary:
            print(f"{process:20} | {category:12} | Entries: {entries:3} | Clicks: {clicks:4} | Keys: {keys:4} | Avg Idle: {idle:.1f}s")
        
        print("\n=== CATEGORY SUMMARY ===")
        cat_summary = self.get_category_summary()
        for category, entries, clicks, keys, idle in cat_summary:
            print(f"{category:15} | Entries: {entries:3} | Clicks: {clicks:4} | Keys: {keys:4} | Avg Idle: {idle:.1f}s")

if __name__ == "__main__":
    analyzer = ActivityAnalyzer()
    analyzer.print_summary()
