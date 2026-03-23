import os
import psutil
import tkinter as tk

try:
    import gpustat
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

REFRESH_MS = 500

BG = "#0f0f0f"
FG = "#ffffff"
DIM = "#444444"
GREEN = "#00ff88"
YELLOW = "#ffd700"
RED = "#ff4444"

FONT = ("Consolas", 10)
FONT_BOLD = ("Consolas", 10, "bold")


def bar_color(percent):
    if percent <= 50: return GREEN
    if percent <= 80: return YELLOW
    return RED



class SystemStats:
    @staticmethod
    def disk_path():
        return "C:\\" if os.name == "nt" else "/"

    @staticmethod
    def get():
        stats = {
            "cpu": psutil.cpu_percent(interval=None),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage(SystemStats.disk_path()).percent,
            "gpus": []
        }
        if GPU_AVAILABLE:
            try:
                for gpu in gpustat.new_query():
                    stats["gpus"].append({
                        "index": gpu.index,
                        "usage": gpu.utilization or 0,
                        "temp": gpu.temperature
                    })
            except Exception as e:
                print(f"[GPU ERROR] {e}")
        return stats

    @staticmethod
    def top_processes():
        procs = []
        total_ram = psutil.virtual_memory().total
        core_count = psutil.cpu_count()
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
            try:
                info = p.info
                username = info['username']
                if not username:
                    continue
                uname = username.lower()
                if uname in ("system", "nt authority\\system", "root"):
                    continue
                info['cpu_percent'] = info['cpu_percent'] / core_count
                info['memory_percent'] = (info['memory_info'].rss / total_ram) * 100
                procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return {
            "cpu": max(procs, key=lambda p: p['cpu_percent'], default=None),
            "ram": max(procs, key=lambda p: p['memory_percent'], default=None)
        }



class BarRow(tk.Frame):
    def __init__(self, master, label_text):
        super().__init__(master, bg=BG)
        self.label = tk.Label(self, text=f"{label_text:<5}", bg=BG, fg=FG, font=FONT, width=5)
        self.label.pack(side="left")
        self.canvas = tk.Canvas(self, width=160, height=12, bg=BG, highlightthickness=0)
        self.canvas.pack(side="left", padx=(4, 6))
        self.percent_label = tk.Label(self, text="  0.0%", bg=BG, fg=FG, font=FONT, width=6)
        self.percent_label.pack(side="left")

    def update(self, percent):
        self.canvas.delete("all")
        filled = int(160 * percent / 100)
        self.canvas.create_rectangle(0, 0, 160, 12, fill=DIM, outline="")
        if filled > 0:
            self.canvas.create_rectangle(0, 0, filled, 12, fill=bar_color(percent), outline="")
        self.percent_label.config(text=f"{percent:5.1f}%", fg=bar_color(percent))


class TopProcessRow(tk.Frame):
    def __init__(self, master, label_text):
        super().__init__(master, bg=BG)
        tk.Label(self, text=f"{label_text:<4}", bg=BG, fg=DIM, font=FONT).pack(side="left")
        self.label = tk.Label(self, text="—", bg=BG, fg=FG, font=FONT)
        self.label.pack(side="left", padx=(4, 0))

    def update(self, text, percent=None):
        self.label.config(text=text)
        if percent is not None:
            self.label.config(fg=bar_color(percent))


class SystemOverlay(tk.Tk):
    def __init__(self):
        super().__init__()
        self._drag_offset = (0, 0)  
        self.title("System Monitor")
        self.configure(bg=BG)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        try:
            self.attributes("-alpha", 0.85)
        except Exception:
            pass

        sw = self.winfo_screenwidth()
        self.geometry(f"+{sw - 280}+10")
        self.bind("<Escape>", lambda e: self.destroy())
        self._make_draggable()

        tk.Label(self, text="● DAVID'S MONITOR", bg=BG, fg=GREEN, font=FONT_BOLD).pack(anchor="w", padx=8, pady=(8, 4))

     
        self.bars = {}
        for key, label in [("cpu", "CPU"), ("ram", "RAM"), ("disk", "Disk")]:
            row = BarRow(self, label)
            row.pack(fill="x", padx=8, pady=2)
            self.bars[key] = row

        tk.Label(self, text="─"*28, bg=BG, fg=DIM, font=FONT).pack(anchor="w", padx=8)

        self.gpu_frame = tk.Frame(self, bg=BG)
        self.gpu_frame.pack(fill="x", padx=8, pady=(0, 4))
        self.gpu_rows = []
        for _ in range(4):
            row = tk.Label(self.gpu_frame, text="", bg=BG, fg=FG, font=FONT)
            row.pack(anchor="w")
            self.gpu_rows.append(row)
        self.no_gpu_label = tk.Label(self.gpu_frame, text="No GPU", bg=BG, fg=DIM, font=FONT)

        tk.Label(self, text="─"*28, bg=BG, fg=DIM, font=FONT).pack(anchor="w", padx=8)

       
        tk.Label(self, text="● TOP PROCESSES", bg=BG, fg=GREEN, font=FONT_BOLD).pack(anchor="w", padx=8, pady=(2, 4))
        self.top_procs = {}
        for key, label in [("cpu", "CPU"), ("ram", "RAM"), ("gpu", "GPU")]:
            row = TopProcessRow(self, label)
            row.pack(fill="x", padx=8)
            self.top_procs[key] = row

        self.update_stats()

    def update_stats(self):
        stats = SystemStats.get()
        procs = SystemStats.top_processes()

        for key in ("cpu", "ram", "disk"):
            self.bars[key].update(stats[key])

       
        if stats["gpus"]:
            self.no_gpu_label.pack_forget()
            for i, row in enumerate(self.gpu_rows):
                if i < len(stats["gpus"]):
                    gpu = stats["gpus"][i]
                    row.config(text=f"GPU{gpu['index']}  {gpu['usage']:5.1f}%   {gpu['temp']}°C", fg=bar_color(gpu['usage']))
                    row.pack(anchor="w")
                else:
                    row.pack_forget()
        else:
            for row in self.gpu_rows: row.pack_forget()
            self.no_gpu_label.pack(anchor="w")

        if procs["cpu"]:
            p = procs["cpu"]
            self.top_procs["cpu"].update(f"{p['name'][:18]:<18}  {p['cpu_percent']:5.1f}%", p['cpu_percent'])
        if procs["ram"]:
            p = procs["ram"]
            self.top_procs["ram"].update(f"{p['name'][:18]:<18}  {p['memory_percent']:5.1f}%", p['memory_percent'])
        self.top_procs["gpu"].update("N/A")

        self.after(REFRESH_MS, self.update_stats)

    def _make_draggable(self):
        self.bind("<ButtonPress-1>", lambda e: setattr(self, "_drag_offset", (e.x, e.y)))
        self.bind("<B1-Motion>", self._drag_move)

    def _drag_move(self, e):
        dx, dy = self._drag_offset
        self.geometry(f"+{self.winfo_x() + e.x - dx}+{self.winfo_y() + e.y - dy}")


if __name__ == "__main__":
    app = SystemOverlay()
    app.mainloop()
