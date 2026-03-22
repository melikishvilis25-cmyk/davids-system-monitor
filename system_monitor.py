

import time
import psutil


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def usage_bar(percent, length=20):
    filled_length = int(length * percent // 100)
    empty_length = length - filled_length

    if percent <= 50:
        color = GREEN
    elif percent <= 80:
        color = YELLOW
    else:
        color = RED

    bar = f"{color}{'█'*filled_length}{RESET}{'-'*empty_length}"
    return f"{bar} {percent:5}%"


print("=== SYSTEM MONITOR ===")
print(f"{'RESOURCE':<10} | {'USAGE'}")
print("-"*30)
print(f"CPU       | ")
print(f"RAM       | ")
print(f"Disk (C:) | ")

try:
    while True:
       
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("C:").percent

       
        print("\033[F"*3, end='')

        
        print(f"CPU       | {usage_bar(cpu_percent)}")
        print(f"RAM       | {usage_bar(ram_percent)}")
        print(f"Disk (C:) | {usage_bar(disk_percent)}")

except KeyboardInterrupt:
    print("\nMonitoring stopped.")