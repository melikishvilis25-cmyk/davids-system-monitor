import os
import psutil
import tkinter as tk

try:
    import gpustat
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


#confing can be changed
#--------------------------------------
REFRESH_MS = 500
BG         = "#0f0f0f"
FG         = "#ffffff"
GREEN      = "#00ff88"
YELLOW     = "#ffd700"
RED        = "#ff4444"
DIM        = "#444444"
FONT       = ("Consolas", 10)
FONT_BOLD  = ("Consolas", 10, "bold")
#---------------------------------------


def get_disk_path():
    return "C:\\" if os.name == "nt" else "/"


def get_system_stats():
    stats = {
        "cpu":  psutil.cpu_percent(interval=None),
        "ram":  psutil.virtual_memory().percent,
        "disk": psutil.disk_usage(get_disk_path()).percent,
        "gpus": []
    }
    if GPU_AVAILABLE:
        try:
            for gpu in gpustat.new_query():
                stats["gpus"].append({
                    "index": gpu.index,
                    "temp":  gpu.temperature,
                    "usage": gpu.utilization or 0
                })
        except Exception as e:
            print("GPU error:", e)
    return stats


def bar_color(percent):
    if percent <= 50:
        return GREEN
    elif percent <= 80:
        return YELLOW
    return RED



class SystemOverlay:
    BAR_W = 160
    BAR_H = 12

    def __init__(self, root):
        self.root = root
        root.title("System Monitor")
        root.configure(bg=BG)
        root.overrideredirect(True)
        root.attributes("-topmost", True)

        try:
            root.attributes("-alpha", 0.85)
        except Exception as e:
            print("Transparency error:", e)

        sw = root.winfo_screenwidth()
        root.geometry(f"+{sw - 280}+10")

        # Escape to quit
        root.bind("<Escape>", lambda e: root.destroy())

        self._build_ui()
        self._make_draggable()
        self.update()

  
    def _build_ui(self):
        pad = dict(padx=8, pady=2)

        tk.Label(self.root, text="● DAVID'S MONITOR",
                 bg=BG, fg=GREEN, font=FONT_BOLD).pack(anchor="w", padx=8, pady=(8, 4))

        self.rows = {}
        for key, label in [("cpu", "CPU"), ("ram", "RAM"), ("disk", "Disk")]:
            row = tk.Frame(self.root, bg=BG)
            row.pack(fill="x", **pad)
            tk.Label(row, text=f"{label:<5}", bg=BG, fg=FG, font=FONT, width=5).pack(side="left")
            cv = tk.Canvas(row, width=self.BAR_W, height=self.BAR_H,
                           bg=BG, highlightthickness=0)
            cv.pack(side="left", padx=(4, 6))
            pct = tk.Label(row, text="  0.0%", bg=BG, fg=FG, font=FONT, width=6)
            pct.pack(side="left")
            self.rows[key] = (cv, pct)

        tk.Label(self.root, text="─" * 28, bg=BG, fg=DIM, font=FONT).pack(anchor="w", padx=8)

        self.gpu_frame = tk.Frame(self.root, bg=BG)
        self.gpu_frame.pack(fill="x", padx=8, pady=(0, 8))

       
        self.gpu_rows = []
        for _ in range(4):
            row = tk.Frame(self.gpu_frame, bg=BG)
            lbl = tk.Label(row, text="", bg=BG, fg=FG, font=FONT)
            lbl.pack(anchor="w")
            self.gpu_rows.append((row, lbl))

        self.no_gpu_label = tk.Label(self.gpu_frame, text="No GPU",
                                     bg=BG, fg=DIM, font=FONT)


    def _draw_bar(self, canvas, percent):
        canvas.delete("all")
        filled = int(self.BAR_W * percent / 100)
        canvas.create_rectangle(0, 0, self.BAR_W, self.BAR_H, fill=DIM, outline="")
        if filled > 0:
            canvas.create_rectangle(0, 0, filled, self.BAR_H,
                                     fill=bar_color(percent), outline="")

 
    def update(self):
        stats = get_system_stats()

        for key in ("cpu", "ram", "disk"):
            pct = stats[key]
            cv, lbl = self.rows[key]
            self._draw_bar(cv, pct)
            lbl.config(text=f"{pct:5.1f}%", fg=bar_color(pct))

        gpus = stats["gpus"]
        if gpus:
            self.no_gpu_label.pack_forget()
            for i, (row, lbl) in enumerate(self.gpu_rows):
                if i < len(gpus):
                    gpu = gpus[i]
                    lbl.config(
                        text=f"GPU{gpu['index']}  {gpu['usage']:5.1f}%   {gpu['temp']}°C",
                        fg=bar_color(gpu['usage'])
                    )
                    row.pack(fill="x")
                else:
                    row.pack_forget()   # hide unused GPU slots
        else:
            for row, _ in self.gpu_rows:
                row.pack_forget()
            self.no_gpu_label.pack(anchor="w")

        self.root.after(REFRESH_MS, self.update)

    
    def _make_draggable(self):
        self.root.bind("<ButtonPress-1>",  self._drag_start)
        self.root.bind("<B1-Motion>",      self._drag_move)

    def _drag_start(self, e):
        self._dx = e.x
        self._dy = e.y

    def _drag_move(self, e):
        x = self.root.winfo_x() + e.x - self._dx
        y = self.root.winfo_y() + e.y - self._dy
        self.root.geometry(f"+{x}+{y}")



if __name__ == "__main__":
    root = tk.Tk()
    SystemOverlay(root)
    root.mainloop()