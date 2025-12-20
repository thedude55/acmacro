# Roblox Window Manager & Automation

Automated Roblox game automation script that manages window positioning, gameplay automation, and image-based detection for various game interactions.

## Features

- **Window Management**: Automatically detects and resizes Roblox window to 700x400 pixels, positioning it in the top-left corner
- **Image Detection**: Uses computer vision to detect game elements and UI components
- **Automated Gameplay**: Automates unit placement, card selection, and game flow
- **Coordinate Tracking**: Utility script to track mouse coordinates on right-click

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Main Automation Script
```bash
python roblox_window_manager.py
```

### Coordinate Tracker
```bash
python cursor_coordinates.py
```

## Requirements

- Windows OS
- Python 3.7+
- Roblox game window
- All required image assets (PNG files) in the project directory

## Notes

- The script works by searching for windows with "Roblox" in the title
- If multiple Roblox windows are open, it will use the first one found
- The window must be visible (not minimized) for the script to work properly
- Image detection uses confidence thresholds (default 0.9)

