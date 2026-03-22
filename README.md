# David's System Monitor

A lightweight real-time system resource monitor for Windows and Linux.  
Starting from v2.0, it runs as a sleek always-on-top desktop overlay instead of the terminal.

---

## Versions

### v2.0 — Desktop Overlay *(current)*
A frameless, transparent overlay that sits in the corner of your screen and stays on top of all windows. Draggable and color-coded.

<img width="385" height="221" alt="image" src="https://github.com/user-attachments/assets/776330fa-8b3b-4f84-8c11-8355c6019c05" />


### v1.0 — Terminal Monitor *(legacy)*
The original console-based version with color-coded ASCII bars. Still useful for **headless servers or SSH sessions** where a display isn't available.  
→ Available under [Releases](https://github.com/melikishvilis25-cmyk/davids-system-monitor/releases/tag/Update)

<img width="823" height="288" alt="preview" src="https://github.com/user-attachments/assets/794291ea-15e7-4ede-9eb8-7858b10b62be" />

---

## Features

- Real-time monitoring of CPU, RAM, and Disk usage
- Optional GPU monitoring (usage + temperature)
- Color-coded bars:
  - 🟢 Green → Normal (0–50%)
  - 🟡 Yellow → Moderate (51–80%)
  - 🔴 Red → High (81–100%)
- Always-on-top frameless window
- Draggable — place it anywhere on screen
- 85% transparency so it doesn't block your work
- Press `Escape` to close
- Cross-platform: Windows & Linux
- Works without a GPU

---

## Requirements

Python 3.10 or newer.

**Required:**
```
pip install psutil
```

**Optional** (GPU monitoring):
```
pip install gpustat
```

**Tkinter** is required for the overlay (v2.0) and comes pre-installed with Python.  
On Linux, if it's missing:
```
# Ubuntu/Debian
sudo apt install python3-tk

# Arch
sudo pacman -S tk
```

---

## Usage

### v2.0 — Desktop Overlay
```
python monitor_gui.py
```
The overlay will appear in the top-right corner of your screen.  
Click and drag it to reposition. Press `Escape` to close.

### v1.0 — Terminal *(headless/SSH)*
```
python monitor_cli.py
```
Press `Ctrl + C` to stop.

---

## Roadmap

- [ ] Per-core CPU usage
- [ ] Network usage (upload/download speed)
- [ ] Log system data to a file
- [ ] Top resource-consuming processes

---

## Notes

- The terminal version (v1.0) works best in terminals that support ANSI colors (PowerShell, Linux terminal, etc.)
- GPU monitoring is optional and only activates if supported hardware and `gpustat` are installed
- Transparency in the overlay requires a compositor on Linux (most modern desktop environments include one)

---

## License

MIT License
