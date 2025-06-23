```markdown
# ActivityScope - Desktop Activity Monitoring Tool

A powerful, privacy-focused desktop activity monitoring system built with Python that tracks mouse clicks, keyboard activity, window focus, and application usage with intelligent categorization.

## Features

- **Real-time Activity Tracking**: Monitor mouse clicks, keyboard presses, and active windows
- **Application Categorization**: Automatically categorizes applications (Development, Web Browsing, Communication, etc.)
- **Idle Time Detection**: Tracks when you're active vs. away from your computer
- **SQLite Database Storage**: Persistent data storage for historical analysis
- **Human-readable Logs**: Text-based logs for easy viewing
- **Privacy-First**: All data stays local on your machine
- **Cross-platform Support**: Works on Windows (with potential for macOS/Linux expansion)

## Requirements

- Python 3.7+
- Windows OS (for current version)
- Administrator privileges (for system-level monitoring)

## Installation

1. **Clone or download this repository**
   ```
   git clone 
   cd ActivityScope
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```
   pip install pynput pywin32 psutil requests
   ```

## Usage

### Basic Activity Tracker
```
python activity_tracker.py
```
- Tracks basic mouse/keyboard activity
- Logs to `activity_log.db` and `usage_log.txt`

### Enhanced Activity Tracker (Recommended)
```
python enhanced_tracker.py
```
- Advanced application categorization
- Real-time console output
- Enhanced logging with activity status
- Logs to `enhanced_activity_log.db` and `enhanced_usage_log.txt`

### View Your Data
```
python view_data.py
```
- Analyze your activity patterns
- View recent activity and process summaries
- Generate usage statistics

## Sample Output

```
ACTIVE | Development  | Code.exe        | Mouse:  5 | Keys: 23 | Idle: 0.2s
ACTIVE | Web Browsing | chrome.exe      | Mouse:  2 | Keys:  8 | Idle: 1.5s
IDLE   | Communication| slack.exe       | Mouse:  0 | Keys:  0 | Idle: 45.2s
```

## File Structure

```
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
├── readme.txt                   # Documentation file
├── activity_log.db              # SQLite database (generated)
├── enhanced_activity_log.db     # Enhanced SQLite database (generated)
├── usage_log.txt               # Human-readable logs (generated)
└── enhanced_usage_log.txt      # Enhanced logs (generated)
```

---

**Author**: Anaya Sharma
```
