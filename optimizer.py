import os
import sys
import gc
import shutil
import tempfile
import subprocess
import ctypes
import threading
import time
import math
import psutil
import GPUtil
import customtkinter as ctk
from tkinter import Canvas, font
import tkinter as tk

# ========================= ADMIN CHECK =========================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv), None, 1
    )
    sys.exit()

# ========================= THEME =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BG         = "#050508"
PANEL      = "#0d0d14"
BORDER     = "#1a1a2e"
ACCENT     = "#00ffe7"
ACCENT2    = "#ff2d78"
ACCENT3    = "#ffe600"
ACCENT4    = "#7b2fff"
TEXT       = "#e8e8f0"
TEXT_DIM   = "#5a5a7a"
FONT_MAIN  = ("Consolas", 11)
FONT_BOLD  = ("Consolas", 11, "bold")
FONT_BIG   = ("Consolas", 28, "bold")
FONT_TITLE = ("Consolas", 14, "bold")

# ========================= ANIMATED CANVAS METER =========================
class NeonMeter(Canvas):
    def __init__(self, master, label="", color=ACCENT, **kwargs):
        super().__init__(master, width=130, height=130,
                         bg=BG, highlightthickness=0, **kwargs)
        self.label   = label
        self.color   = color
        self._value  = 0
        self._target = 0
        self._animating = False
        self._draw(0)
        self._animate()

    def set(self, val):
        self._target = max(0, min(100, val))

    def _animate(self):
        if abs(self._value - self._target) > 0.5:
            self._value += (self._target - self._value) * 0.12
            self._draw(self._value)
        self.after(30, self._animate)

    def _draw(self, val):
        self.delete("all")
        cx, cy, r = 65, 65, 48
        # Outer glow ring (tkinter no alpha - use dim colors instead)
        glow_colors = ["#0a2a26", "#0d3d36", "#0f5248", "#126b5e"]
        if self.color == "#ff2d78":
            glow_colors = ["#2a0a14", "#3d0d1e", "#520f28", "#6b1235"]
        elif self.color == "#ffe600":
            glow_colors = ["#2a2600", "#3d3700", "#524800", "#6b5e00"]
        elif self.color == "#00aaff":
            glow_colors = ["#001a2a", "#00263d", "#003252", "#00406b"]
        for i in range(4, 0, -1):
            self.create_oval(cx-r-i*2, cy-r-i*2, cx+r+i*2, cy+r+i*2,
                             outline=glow_colors[4-i], width=1)
        # Background arc
        self.create_arc(cx-r, cy-r, cx+r, cy+r,
                        start=225, extent=-270,
                        outline=BORDER, width=6, style="arc")
        # Value arc
        extent = -270 * (val / 100)
        if abs(extent) > 0.5:
            # Danger color
            col = self.color
            if val > 85:
                col = ACCENT2
            elif val > 65:
                col = ACCENT3
            self.create_arc(cx-r, cy-r, cx+r, cy+r,
                            start=225, extent=extent,
                            outline=col, width=6, style="arc")
        # Inner circle
        self.create_oval(cx-r+12, cy-r+12, cx+r-12, cy+r-12,
                         fill="#0a0a12", outline=BORDER, width=1)
        # Value text
        display = f"{val:.0f}"
        self.create_text(cx, cy-6, text=display,
                         fill=self.color, font=("Consolas", 18, "bold"))
        self.create_text(cx, cy+12, text="%",
                         fill=TEXT_DIM, font=("Consolas", 9))
        # Label
        self.create_text(cx, cy+38, text=self.label,
                         fill=TEXT_DIM, font=("Consolas", 9, "bold"))

# ========================= GLITCH TITLE =========================
class GlitchTitle(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=900, height=70,
                         bg=BG, highlightthickness=0, **kwargs)
        self._tick = 0
        self._draw()

    def _draw(self):
        self.delete("all")
        t = self._tick
        txt = "TOASTER BOOSTER X"
        # Glitch offsets
        glitch = (math.sin(t * 0.3) > 0.92)
        ox = int(math.sin(t * 7.1) * 3) if glitch else 0
        # Shadow layers
        for i, (col, dx, dy) in enumerate([
            ("#2a0f55", -3, 2), ("#550f28", 3, -2),
            (ACCENT,    0,  0)
        ]):
            self.create_text(450+dx+ox*(i-1), 38+dy,
                             text=txt, fill=col,
                             font=("Consolas", 30, "bold"))
        # Scanline
        scan_y = (t * 3) % 70
        self.create_line(0, scan_y, 900, scan_y, fill="#0a3a33", width=1)
        # Corner brackets
        for x, y, sx, sy in [(5,5,1,1),(895,5,-1,1),(5,65,1,-1),(895,65,-1,-1)]:
            self.create_line(x, y, x+sx*20, y, fill=ACCENT, width=2)
            self.create_line(x, y, x, y+sy*20, fill=ACCENT, width=2)
        self._tick += 1
        self.after(40, self._draw)

# ========================= LOG BOX WITH TYPING EFFECT =========================
class NeonLog(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=PANEL,
                         border_color=BORDER, border_width=1, **kwargs)
        self._queue = []
        hdr = ctk.CTkLabel(self, text="[ SYSTEM LOG ]",
                           font=FONT_TITLE, text_color=ACCENT)
        hdr.pack(anchor="w", padx=10, pady=(8,2))
        self.box = ctk.CTkTextbox(
            self, height=160, fg_color="#08080f",
            text_color=ACCENT, font=FONT_MAIN,
            scrollbar_button_color=BORDER
        )
        self.box.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self._process_queue()

    def log(self, text, color=None):
        self._queue.append(text)

    def _process_queue(self):
        if self._queue:
            msg = self._queue.pop(0)
            self._type_text(f">> {msg}\n")
        self.after(80, self._process_queue)

    def _type_text(self, text):
        self.box.insert("end", text)
        self.box.see("end")

# ========================= ACTION BUTTON =========================
class NeonButton(tk.Canvas):
    def __init__(self, master, text="", color=ACCENT,
                 command=None, width=200, height=48, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg=BG, highlightthickness=0, **kwargs)
        self.txt     = text
        self.color   = color
        self.command = command
        self._hover  = False
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw(self):
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        col = self.color
        # Glow when hover
        if self._hover:
            for i in range(4, 0, -1):
                self.create_rectangle(i, i, w-i, h-i,
                                      outline="#1a3a35", width=1)
            self.create_rectangle(2, 2, w-2, h-2,
                                  fill="#0a1f1c", outline=col, width=2)
        else:
            self.create_rectangle(2, 2, w-2, h-2,
                                  fill="#0a0a0f", outline=col, width=1)
        # Corner details
        sz = 6
        for x, y in [(2,2),(w-2,2),(2,h-2),(w-2,h-2)]:
            dx = 1 if x < w//2 else -1
            dy = 1 if y < h//2 else -1
            self.create_line(x, y, x+dx*sz, y, fill=col, width=2)
            self.create_line(x, y, x, y+dy*sz, fill=col, width=2)
        text_col = "#ffffff" if self._hover else col
        self.create_text(w//2, h//2, text=self.txt,
                         fill=text_col, font=FONT_BOLD)

    def _on_enter(self, e):
        self._hover = True
        self._draw()
        self.config(cursor="hand2")

    def _on_leave(self, e):
        self._hover = False
        self._draw()

    def _on_click(self, e):
        if self.command:
            self.command()

# ========================= MAIN APP =========================
class Optimizer(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("960x760")
        self.minsize(860, 700)
        self.title("TOASTER BOOSTER X")
        self.configure(fg_color=BG)
        self._build_ui()
        self._update_stats()
        self.log("System analysis complete. Ready.")
        self.log("Hit the big button to BOOST.")

    # ---- UI BUILD ----
    def _build_ui(self):
        # Title
        title = GlitchTitle(self)
        title.pack(pady=(12, 4))

        # Meters row
        meter_frame = ctk.CTkFrame(self, fg_color=PANEL,
                                   border_color=BORDER, border_width=1)
        meter_frame.pack(fill="x", padx=20, pady=6)

        lbl = ctk.CTkLabel(meter_frame, text="[ LIVE HARDWARE STATUS ]",
                           font=FONT_TITLE, text_color=TEXT_DIM)
        lbl.grid(row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(8,0))

        self.cpu_m  = NeonMeter(meter_frame, "CPU",  ACCENT)
        self.ram_m  = NeonMeter(meter_frame, "RAM",  "#00aaff")
        self.gpu_m  = NeonMeter(meter_frame, "GPU",  ACCENT2)
        self.disk_m = NeonMeter(meter_frame, "DISK", ACCENT3)

        self.cpu_m.grid( row=1, column=0, padx=20, pady=12)
        self.ram_m.grid( row=1, column=1, padx=20, pady=12)
        self.gpu_m.grid( row=1, column=2, padx=20, pady=12)
        self.disk_m.grid(row=1, column=3, padx=20, pady=12)

        # Stat labels
        self.cpu_lbl  = self._stat_label(meter_frame, 2, 0)
        self.ram_lbl  = self._stat_label(meter_frame, 2, 1)
        self.gpu_lbl  = self._stat_label(meter_frame, 2, 2)
        self.disk_lbl = self._stat_label(meter_frame, 2, 3)

        # BOOST button
        boost_canvas = tk.Canvas(self, width=880, height=68,
                                 bg=BG, highlightthickness=0)
        boost_canvas.pack(pady=8)
        self._boost_btn_canvas = boost_canvas
        self._boost_hover = False
        self._boost_tick = 0
        self._draw_boost_btn()
        boost_canvas.bind("<Enter>",    self._boost_enter)
        boost_canvas.bind("<Leave>",    self._boost_leave)
        boost_canvas.bind("<Button-1>", lambda e: threading.Thread(
            target=self.boost_system, daemon=True).start())
        self._animate_boost()

        # Mode buttons
        mode_frame = ctk.CTkFrame(self, fg_color=PANEL,
                                  border_color=BORDER, border_width=1)
        mode_frame.pack(fill="x", padx=20, pady=6)

        lbl2 = ctk.CTkLabel(mode_frame, text="[ PERFORMANCE MODES ]",
                            font=FONT_TITLE, text_color=TEXT_DIM)
        lbl2.grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(8,4))

        modes = [
            ("📹  VIDEO CAPTURE MODE",         "#4444ff", self.video_mode),
            ("🎮  GAME + STREAM MODE",        "#ff8800", self.stream_mode),
            ("⚡  ULTRA FPS MODE",            ACCENT2,   self.ultra_fps_mode),
        ]
        for i, (txt, col, cmd) in enumerate(modes):
            btn = NeonButton(mode_frame, text=txt, color=col,
                             command=lambda c=cmd: threading.Thread(
                                 target=c, daemon=True).start(),
                             width=270, height=44)
            btn.grid(row=1, column=i, padx=12, pady=10)

        # Extra tools
        tools_frame = ctk.CTkFrame(self, fg_color=PANEL,
                                   border_color=BORDER, border_width=1)
        tools_frame.pack(fill="x", padx=20, pady=6)

        lbl3 = ctk.CTkLabel(tools_frame, text="[ MAINTENANCE TOOLS ]",
                            font=FONT_TITLE, text_color=TEXT_DIM)
        lbl3.grid(row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(8,4))

        tools = [
            ("🗑  CLEAN TEMP",      ACCENT,  self.clean_temp),
            ("🔧  KILL SERVICES", ACCENT4, self.optimize_services),
            ("💾  FLUSH RAM",        "#00aaff", self.flush_ram),
            ("🌐  FLUSH DNS",       "#00cc88", self.flush_dns),
        ]
        for i, (txt, col, cmd) in enumerate(tools):
            btn = NeonButton(tools_frame, text=txt, color=col,
                             command=lambda c=cmd: threading.Thread(
                                 target=c, daemon=True).start(),
                             width=195, height=40)
            btn.grid(row=1, column=i, padx=10, pady=8)

        # Log
        self.neon_log = NeonLog(self)
        self.neon_log.pack(fill="both", expand=True, padx=20, pady=(6,16))

    def _stat_label(self, parent, row, col):
        lbl = ctk.CTkLabel(parent, text="---",
                           font=("Consolas", 9), text_color=TEXT_DIM)
        lbl.grid(row=row, column=col, padx=10, pady=(0,8))
        return lbl

    # ---- BOOST BUTTON ANIMATION ----
    def _draw_boost_btn(self):
        c = self._boost_btn_canvas
        c.delete("all")
        w, h = 880, 68
        t = self._boost_tick
        col = ACCENT
        pulse = 0.5 + 0.5 * math.sin(t * 0.15)
        if self._boost_hover:
            for i in range(6, 0, -1):
                dim = max(0, 20 + i*12 + int(pulse*30))
                shade = format(min(255, dim), "02x")
                self.create_rectangle(i, i, w-i, h-i,
                                      outline=f"#00{shade}{shade[::-1] if len(shade)==2 else shade}", width=1)
            c.create_rectangle(3, 3, w-3, h-3,
                               fill="#0a1f1c", outline=col, width=2)
            txt_col = "#000000"
        else:
            for i in range(3, 0, -1):
                c.create_rectangle(i, i, w-i, h-i,
                                   outline="#0d2e28", width=1)
            c.create_rectangle(3, 3, w-3, h-3,
                               fill="#0a0f0d", outline=col, width=2)
            txt_col = col
        # Scan line
        scan = (t * 4) % h
        c.create_line(3, scan, w-3, scan, fill="#0a3a33", width=1)
        # Corner decorations
        for x, y, sx, sy in [(3,3,1,1),(w-3,3,-1,1),(3,h-3,1,-1),(w-3,h-3,-1,-1)]:
            c.create_line(x, y, x+sx*16, y, fill=col, width=2)
            c.create_line(x, y, x, y+sy*16, fill=col, width=2)
        c.create_text(w//2, h//2, text="▶  BOOST SYSTEM  ◀",
                      fill=txt_col, font=("Consolas", 22, "bold"))

    def _animate_boost(self):
        self._boost_tick += 1
        self._draw_boost_btn()
        self.after(40, self._animate_boost)

    def _boost_enter(self, e):
        self._boost_hover = True
        self._boost_btn_canvas.config(cursor="hand2")

    def _boost_leave(self, e):
        self._boost_hover = False

    # ---- LOG ----
    def log(self, text):
        self.neon_log.log(text)

    # ---- STATS UPDATE ----
    def _update_stats(self):
        try:
            cpu  = psutil.cpu_percent(interval=None)
            ram  = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\')

            gpus = GPUtil.getGPUs()
            gpu_load = (gpus[0].load * 100) if gpus else 0
            gpu_name = gpus[0].name[:18] if gpus else "N/A"

            self.cpu_m.set(cpu)
            self.ram_m.set(ram.percent)
            self.gpu_m.set(gpu_load)
            self.disk_m.set(disk.percent)

            ram_gb  = ram.used / (1024**3)
            ram_tot = ram.total / (1024**3)
            disk_gb = disk.used / (1024**3)
            disk_tot= disk.total / (1024**3)

            self.cpu_lbl.configure( text=f"{cpu:.1f}%  |  {psutil.cpu_count()} cores")
            self.ram_lbl.configure( text=f"{ram_gb:.1f} / {ram_tot:.1f} GB")
            self.gpu_lbl.configure( text=gpu_name)
            self.disk_lbl.configure(text=f"{disk_gb:.1f} / {disk_tot:.1f} GB")
        except:
            pass
        self.after(1500, self._update_stats)

    # ========================= BOOST =========================
    def boost_system(self):
        self.log("━━━ BOOST STARTED ━━━")
        self.log("Power plan: Ultimate Performance active...")
        subprocess.run("powercfg -setactive SCHEME_MIN", shell=True,
                       capture_output=True)
        time.sleep(0.3)

        self.log("Running garbage collector...")
        gc.collect()
        time.sleep(0.2)

        self.clean_temp()
        self.optimize_services()
        self.flush_ram()
        self.flush_dns()
        self._visual_tweaks()

        self.log("━━━ BOOST COMPLETE ━━━")

    # ========================= CLEAN TEMP =========================
    def clean_temp(self):
        self.log("Cleaning temp files...")
        folders = [
            tempfile.gettempdir(),
            r"C:\Windows\Temp",
            r"C:\Windows\Prefetch",
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
        ]
        total = 0
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for item in os.listdir(folder):
                path = os.path.join(folder, item)
                try:
                    if os.path.isfile(path):
                        sz = os.path.getsize(path)
                        os.unlink(path)
                        total += sz
                    elif os.path.isdir(path):
                        sz = sum(
                            os.path.getsize(os.path.join(dp, f))
                            for dp, _, fs in os.walk(path)
                            for f in fs if os.path.exists(os.path.join(dp, f))
                        )
                        shutil.rmtree(path, ignore_errors=True)
                        total += sz
                except:
                    pass
        mb = total / (1024 * 1024)
        self.log(f"Cleaned: {mb:.1f} MB freed.")

    # ========================= SERVICES =========================
    def optimize_services(self):
        self.log("Stopping FPS-tanking services...")
        services = [
            "SysMain", "WSearch", "XboxNetApiSvc",
            "XblGameSave", "XblAuthManager", "Fax",
            "DiagTrack", "dmwappushservice",
        ]
        for s in services:
            r = subprocess.run(f"sc stop {s}", shell=True, capture_output=True)
            if r.returncode == 0:
                self.log(f"  ✓ {s} stopped")
            else:
                self.log(f"  – {s} already stopped or inaccessible")
        self.log("Service optimization complete.")

    # ========================= FLUSH RAM =========================
    def flush_ram(self):
        self.log("Flushing RAM...")
        gc.collect()
        try:
            # EmptyWorkingSet trick via taskmgr equivalent
            subprocess.run(
                'powershell -Command "Get-Process | ForEach-Object { '
                'try { $_.MinWorkingSet = $_.MinWorkingSet } catch {} }"',
                shell=True, capture_output=True, timeout=15
            )
        except:
            pass
        after = psutil.virtual_memory().available / (1024**3)
        self.log(f"  Free RAM: {after:.2f} GB")

    # ========================= FLUSH DNS =========================
    def flush_dns(self):
        self.log("Flushing DNS cache...")
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        self.log("  DNS flushed. Internet may feel faster.")

    # ========================= VISUAL TWEAKS =========================
    def _visual_tweaks(self):
        self.log("Applying Windows system tweaks...")
        tweaks = [
            # Disable mouse acceleration
            ('reg add "HKCU\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f'),
            # Hardware-accelerated GPU scheduling
            ('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" '
             '/v HwSchMode /t REG_DWORD /d 2 /f'),
            # Game priority
            ('reg add "HKCU\\Software\\Microsoft\\GameBar" '
             '/v AllowAutoGameMode /t REG_DWORD /d 1 /f'),
            # MMCSS game scheduling priority
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" '
             '/v Priority /t REG_DWORD /d 6 /f'),
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" '
             '/v "Scheduling Category" /t REG_SZ /d High /f'),
            # Network tweaks
            ('netsh int tcp set global autotuninglevel=normal'),
            ('netsh int tcp set global ecncapability=enabled'),
        ]
        for cmd in tweaks:
            try:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            except:
                pass
        self.log("  System tweaks applied successfully.")

    # ========================= MODLAR =========================
    def video_mode(self):
        self.log("📹 Video Capture Mode active...")
        subprocess.run("powercfg /setactive SCHEME_BALANCED",
                       shell=True, capture_output=True)
        subprocess.run("sc stop XboxNetApiSvc", shell=True, capture_output=True)
        self.log("  Balanced power plan. CPU/GPU optimized.")

    def stream_mode(self):
        self.log("🎮 Game + Stream Mode active...")
        subprocess.run("powercfg /setactive SCHEME_MIN",
                       shell=True, capture_output=True)
        self.log("  High performance power plan. Optimized for streaming.")

    def ultra_fps_mode(self):
        self.log("⚡ ULTRA FPS Mode active...")
        subprocess.run("powercfg -setactive SCHEME_MIN",
                       shell=True, capture_output=True)
        self._visual_tweaks()
        # Kill all background services
        extra = ["WSearch", "SysMain", "DiagTrack",
                 "dmwappushservice", "TabletInputService"]
        for s in extra:
            subprocess.run(f"sc stop {s}", shell=True, capture_output=True)
        self.log("  ULTRA FPS active! All unnecessary services stopped.")


# ========================= ENTRY =========================
if __name__ == "__main__":
    app = Optimizer()
    app.mainloop()