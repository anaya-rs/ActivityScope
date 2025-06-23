================================================================================
                            ACTIVITYSCOPE
                    Desktop Activity Monitoring Tool
================================================================================

Author: Anaya Sharma
Version: 1.0
Date: June 2025

================================================================================
DESCRIPTION
================================================================================

ActivityScope is a powerful, privacy-focused desktop activity monitoring system 
built with Python. It tracks mouse clicks, keyboard activity, window focus, and 
application usage with intelligent categorization.

================================================================================
FEATURES
================================================================================

* Real-time Activity Tracking - Monitor mouse clicks, keyboard presses, and 
  active windows
* Application Categorization - Automatically categorizes applications 
  (Development, Web Browsing, Communication, etc.)
* Idle Time Detection - Tracks when you're active vs. away from your computer
* SQLite Database Storage - Persistent data storage for historical analysis
* Human-readable Logs - Text-based logs for easy viewing
* Privacy-First - All data stays local on your machine
* Cross-platform Support - Works on Windows (with potential for macOS/Linux)

================================================================================
REQUIREMENTS
================================================================================

* Python 3.7 or higher
* Windows OS (for current version)
* Administrator privileges (for system-level monitoring)

================================================================================
INSTALLATION
================================================================================

1. Create a virtual environment:
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:
   pip install pynput pywin32 psutil requests

================================================================================
USAGE
================================================================================

Basic Activity Tracker:
   python activity_tracker.py

Enhanced Activity Tracker (Recommended):
   python enhanced_tracker.py

View Your Data:
   python view_data.py

================================================================================
FILES GENERATED
================================================================================

* activity_log.db - SQLite database with basic tracking data
* enhanced_activity_log.db - SQLite database with enhanced tracking data
* usage_log.txt - Human-readable basic logs
* enhanced_usage_log.txt - Human-readable enhanced logs

================================================================================
SAMPLE OUTPUT
================================================================================

ACTIVE | Development  | Code.exe        | Mouse:  5 | Keys: 23 | Idle: 0.2s
ACTIVE | Web Browsing | chrome.exe      | Mouse:  2 | Keys:  8 | Idle: 1.5s
IDLE   | Communication| slack.exe       | Mouse:  0 | Keys:  0 | Idle: 45.2s

================================================================================
APPLICATION CATEGORIES
================================================================================

* Development: VS Code, Visual Studio, IDEs
* Web Browsing: Chrome, Firefox, Edge
* Communication: Slack, Teams, Discord
* Text Editing: Notepad, Notepad++
* Email: Outlook, Thunderbird
* File Management: Windows Explorer
* Terminal: Command Prompt, PowerShell
* Other: Uncategorized applications

================================================================================
CUSTOMIZATION
================================================================================

To add new application categories, edit the app_categories dictionary in 
enhanced_tracker.py:

self.app_categories = {
    "your_app.exe": "Your Category",
    "another_app.exe": "Another Category",
}

To adjust idle time threshold, modify this line in log_activity method:
is_active = idle_time < 30  # Change 30 to your preferred seconds

================================================================================
PRIVACY & ETHICS
================================================================================

* Local Data Only: All tracking data remains on your local machine
* No Keylogging: Tracks key press counts, not actual keystrokes
* Transparent: Open source code for full transparency
* Consent Required: Only use on machines you own or have explicit permission

================================================================================
TROUBLESHOOTING
================================================================================

Common Issues:

1. "Module 'win32gui' has no attribute 'GetWindowThreadProcessId'"
   Solution: Code uses win32process.GetWindowThreadProcessId() - ensure latest version

2. "Permission Denied" errors
   Solution: Run as Administrator for full system access

3. "Unknown" applications showing
   Solution: Check if application process name is in app_categories dictionary

================================================================================
FILE STRUCTURE
================================================================================

ACTIVITYTRACKERPROJ/
├── venv/                        # Virtual environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── .gitignore
│   └── pyvenv.cfg
├── activity_tracker.py          # Basic activity tracker
├── enhanced_tracker.py          # Advanced tracker with categorization
├── view_data.py                 # Data analysis and viewing tool
├── readme.txt                   # This documentation file
├── activity_log.db              # SQLite database (generated)
├── enhanced_activity_log.db     # Enhanced SQLite database (generated)
├── usage_log.txt               # Human-readable logs (generated)
└── enhanced_usage_log.txt      # Enhanced logs (generated)

================================================================================
END OF README
================================================================================
