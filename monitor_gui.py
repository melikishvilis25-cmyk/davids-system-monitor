import os
import psutil
import tkinter as tk

try:
    import gpustat
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False



REFRESH_MS = 500
BG         = "#0f0f0f"
FG         = "#ffffff"
GREEN      = "#00ff88"
YELLOW     = "#ffd700"
RED        = "#ff4444"
DIM        = "#444444"
FONT       = ("Consolas", 10)
FONT_BOLD  = ("Consolas", 10, "bold")



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


def get_top_processes():
    procs = []
    total_ram = psutil.virtual_memory().total
    core_count = psutil.cpu_count()

    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
        try:
            info = p.info

            # skip system/kernel processes
            if not info['username']:
                continue
            if info['username'] in ("SYSTEM", "NT AUTHORITY\\SYSTEM", "root"):
                continue

            info['cpu_percent']    = info['cpu_percent'] / core_count
            info['memory_percent'] = (info['memory_info'].rss / total_ram) * 100
            procs.append(info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_cpu = max(procs, key=lambda p: p['cpu_percent'],    default=None)
    top_ram = max(procs, key=lambda p: p['memory_percent'], default=None)

    return {
        "cpu": top_cpu,
        "ram": top_ram,
    }


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

        root.bind("<Escape>", lambda e: root.destroy())

        self._build_ui()
        self._make_draggable()
        self.update()


    def _build_ui(self):
        pad = dict(padx=8, pady=2)

   
        tk.Label(self.root, text="● DAVID'S MONITOR",
                 bg=BG, fg=GREEN, font=FONT_BOLD).pack(anchor="w", padx=8, pady=(8, 4))

        # CPU / RAM / Disk bars
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
        self.gpu_frame.pack(fill="x", padx=8, pady=(0, 4))

        
        self.gpu_rows = []
        for _ in range(4):
            row = tk.Frame(self.gpu_frame, bg=BG)
            lbl = tk.Label(row, text="", bg=BG, fg=FG, font=FONT)
            lbl.pack(anchor="w")
            self.gpu_rows.append((row, lbl))

        self.no_gpu_label = tk.Label(self.gpu_frame, text="No GPU",
                                     bg=BG, fg=DIM, font=FONT)

        
        tk.Label(self.root, text="─" * 28, bg=BG, fg=DIM, font=FONT).pack(anchor="w", padx=8)

        proc_frame = tk.Frame(self.root, bg=BG)
        proc_frame.pack(fill="x", padx=8, pady=(0, 8))

        tk.Label(proc_frame, text="● TOP PROCESSES",
                 bg=BG, fg=GREEN, font=FONT_BOLD).pack(anchor="w", pady=(2, 4))

        self.proc_labels = {}
        for key, label in [("cpu", "CPU"), ("ram", "RAM"), ("gpu", "GPU")]:
            row = tk.Frame(proc_frame, bg=BG)
            row.pack(fill="x")
            tk.Label(row, text=f"{label:<4}", bg=BG, fg=DIM, font=FONT).pack(side="left")
            lbl = tk.Label(row, text="—", bg=BG, fg=FG, font=FONT)
            lbl.pack(side="left", padx=(4, 0))
            self.proc_labels[key] = lbl

   
    def _draw_bar(self, canvas, percent):
        canvas.delete("all")
        filled = int(self.BAR_W * percent / 100)
        canvas.create_rectangle(0, 0, self.BAR_W, self.BAR_H, fill=DIM, outline="")
        if filled > 0:
            canvas.create_rectangle(0, 0, filled, self.BAR_H,
                                     fill=bar_color(percent), outline="")

    
    def update(self):
        stats = get_system_stats()
        procs = get_top_processes()

        # CPU / RAM / Disk bars
        for key in ("cpu", "ram", "disk"):
            pct = stats[key]
            cv, lbl = self.rows[key]
            self._draw_bar(cv, pct)
            lbl.config(text=f"{pct:5.1f}%", fg=bar_color(pct))

        # GPU rows
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
                    row.pack_forget()
        else:
            for row, _ in self.gpu_rows:
                row.pack_forget()
            self.no_gpu_label.pack(anchor="w")

        # Top processes
        if procs["cpu"]:
            p = procs["cpu"]
            self.proc_labels["cpu"].config(
                text=f"{p['name'][:18]:<18}  {p['cpu_percent']:5.1f}%",
                fg=bar_color(p['cpu_percent'])
            )

        if procs["ram"]:
            p = procs["ram"]
            self.proc_labels["ram"].config(
                text=f"{p['name'][:18]:<18}  {p['memory_percent']:5.1f}%",
                fg=bar_color(p['memory_percent'])
            )

       
        self.proc_labels["gpu"].config(text="N/A", fg=DIM)

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
