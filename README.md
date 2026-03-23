# David's System Monitor
A lightweight real-time system resource monitor for Windows and Linux.  
Starting from v2.0, it runs as a sleek always-on-top desktop overlay instead of the terminal.

---

## Versions

### v2.0.2 - Bug Fixes *(current)*
Fixed CPU usage showing incorrect high values by normalizing per core count. Fixed RAM process detection calculating memory manually from RSS instead of relying on stale psutil values. Fixed system process filter to be case insensitive so it works correctly on both Windows and Linux. GPU errors now print to console instead of silently failing.

### v2.0.1 - Desktop Overlay
Added top process tracking - shows the highest CPU and RAM consuming process in real-time. Still as lightweight as before.
GPU top process tracking is not yet supported and will be added in v2.1.

<img width="343" height="330" alt="Screenshot 2026-03-23 195002" src="https://github.com/user-attachments/assets/e9dbbeb9-1040-47f4-9012-4922340b2a9e" />

### v2.0 - Desktop Overlay
A frameless, transparent overlay that sits in the corner of your screen and stays on top of all windows. Draggable and color-coded.

<img width="385" height="221" alt="image" src="https://github.com/user-attachments/assets/776330fa-8b3b-4f84-8c11-8355c6019c05" />

### v1.0 - Terminal Monitor *(legacy)*
The original console-based version with color-coded ASCII bars. Still useful for **headless servers or SSH sessions** where a display isn't available.  
Available under [Releases](https://github.com/melikishvilis25-cmyk/davids-system-monitor/releases/tag/Update)

<img width="823" height="288" alt="preview" src="https://github.com/user-attachments/assets/794291ea-15e7-4ede-9eb8-7858b10b62be" />

---

## Features

- Real-time monitoring of CPU, RAM, and Disk usage
- Top process tracking - highest CPU and RAM consuming process
- Optional GPU monitoring (usage + temperature)
- GPU top process tracking not yet supported - coming in v2.1
- Color-coded bars:
  - 🟢 Green - Normal (0-50%)
  - 🟡 Yellow - Moderate (51-80%)
  - 🔴 Red - High (81-100%)
- Always-on-top frameless window
- Draggable - place it anywhere on screen
- 85% transparency so it doesn't block your work
- Press `Escape` to close
- Cross-platform: Windows & Linux
- Works without a GPU

---

## Installation

### Easy Install (Recommended)

**Windows** - just double-click `install.bat`  
It will automatically create a virtual environment and install all dependencies.

**Linux** - run in terminal:
```
chmod +x install.sh
./install.sh
```

### Manual Install

**Required:**
```
pip install psutil
```

**Optional** (GPU monitoring):
```
pip install gpustat
```

### Advanced (requirements.txt)
For those who prefer managing dependencies manually:
```
pip install -r requirements.txt
```

**Tkinter** comes pre-installed with Python.  
On Linux, if it's missing:
```
# Ubuntu/Debian
sudo apt install python3-tk

# Arch
sudo pacman -S tk
```

Python 3.10 or newer required.

---

## Usage

### v2.0 - Desktop Overlay
```
python monitor_gui.py
```
The overlay will appear in the top-right corner of your screen.  
Click and drag it to reposition. Press `Escape` to close.

> If you used `install.bat` or `install.sh`, activate the virtual environment first:
> ```
> # Windows
> venv\Scripts\activate
>
> # Linux
> source venv/bin/activate
> ```

### v1.0 - Terminal (headless/SSH)
```
python monitor_cli.py
```
Press `Ctrl + C` to stop.

---

## Roadmap

- [ ] GPU top process tracking (v2.1)
- [ ] Per-core CPU usage
- [ ] Network usage (upload/download speed)
- [ ] Log system data to a file

---

## Notes

- The terminal version (v1.0) works best in terminals that support ANSI colors (PowerShell, Linux terminal, etc.)
- GPU monitoring only activates if supported hardware and `gpustat` are installed
- Transparency in the overlay requires a compositor on Linux (most modern desktop environments include one)
- GPU top process tracking is not yet supported - coming in v2.1

---

## License

MIT License
