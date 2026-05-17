# ⚡ ToasterBoosterX

> **A free, open-source Windows optimizer built for low-end PCs — because everyone deserves a fast computer.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Admin](https://img.shields.io/badge/Requires-Admin-red?style=for-the-badge)

---

## 🖥️ What is ToasterBoosterX?

ToasterBoosterX is a **real-time Windows performance optimizer** with a cyberpunk neon UI. It boosts FPS, frees up RAM, cleans junk files, kills background services, and applies system tweaks — all in one click.

Designed especially for **potato PCs and toaster laptops** that struggle to run games or apps smoothly.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚀 **One-Click BOOST** | Applies all optimizations at once |
| 📊 **Live Hardware Meters** | Real-time CPU / RAM / GPU / DISK monitoring |
| 🗑️ **Temp Cleaner** | Clears Windows temp folders and frees disk space |
| 🔧 **Service Killer** | Stops FPS-tanking background services |
| 💾 **RAM Flush** | Forces working set cleanup across all processes |
| 🌐 **DNS Flush** | Clears DNS cache for faster internet |
| 🎮 **Ultra FPS Mode** | Max performance power plan + registry tweaks |
| 📹 **Video Mode** | Balanced plan optimized for recording/streaming |
| ⚡ **Stream Mode** | High performance for gaming + streaming simultaneously |
| 🖱️ **Mouse Acceleration OFF** | Disables Windows mouse acceleration for precise aim |
| 🎯 **GPU Hardware Scheduling** | Enables HAGS for better GPU utilization |
| 🏆 **MMCSS Game Priority** | Sets high scheduling priority for games |
| 🌍 **TCP Network Tweaks** | Optimizes TCP auto-tuning and ECN |

---

## 🎨 UI Preview

```
╔══════════════════════════════════════════════╗
║   TOASTER BOOSTER X   (glitch animated)      ║
╠══════════════════════════════════════════════╣
║  [CPU ◉]  [RAM ◉]  [GPU ◉]  [DISK ◉]        ║
║   neon arc meters with smooth animation      ║
╠══════════════════════════════════════════════╣
║        ▶  BOOST SİSTEMİ  ◀  (pulsing)       ║
╠══════════════════════════════════════════════╣
║  [VIDEO MODE]  [STREAM MODE]  [ULTRA FPS]    ║
║  [TEMP CLEAN]  [SERVICES]  [RAM]  [DNS]      ║
╠══════════════════════════════════════════════╣
║  >> SYSTEM LOG (live output)                 ║
╚══════════════════════════════════════════════╝
```

> Dark cyberpunk aesthetic — neon green/cyan/pink/yellow on black

---

## 🚀 Quick Start

### Option 1 — Run from source

```bash
# 1. Clone the repo
git clone https://github.com/Ast1Kaan/ToasterBoosterX.git
cd ToasterBoosterX

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run (must be run as Administrator)
python optimizer.py
```

> ⚠️ **Must be run as Administrator.** The app will auto-request admin privileges on launch.

### Option 2 — Build your own EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --uac-admin --name "ToasterBoosterX" --collect-all customtkinter --hidden-import psutil --hidden-import GPUtil optimizer.py
```

The `.exe` will appear in the `dist/` folder. No Python required on the target machine.

---

## 📦 Requirements

```
customtkinter==5.2.2
psutil==5.9.8
GPUtil==1.4.0
Pillow==10.3.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## ⚙️ What Does BOOST Actually Do?

When you hit the **BOOST** button, the following happens in order:

1. Switches power plan to **Ultimate Performance**
2. Runs Python garbage collector (`gc.collect()`)
3. Clears all **Temp folders** (`%TEMP%`, `C:\Windows\Temp`, `Prefetch`, `%LOCALAPPDATA%\Temp`)
4. Stops background **Windows services** that tank FPS:
   - `SysMain` (Superfetch), `WSearch`, `XboxNetApiSvc`, `XblGameSave`, `XblAuthManager`, `Fax`, `DiagTrack`, `dmwappushservice`
5. **Flushes RAM** working sets across all processes
6. **Flushes DNS** cache
7. Applies **registry tweaks**:
   - Mouse acceleration OFF
   - Hardware-Accelerated GPU Scheduling (HAGS) ON
   - Game Bar auto-mode ON
   - MMCSS game scheduling priority: HIGH
   - TCP auto-tuning + ECN enabled

---

## ⚠️ Disclaimer

- This tool modifies **Windows registry** and **stops system services.**
- Some services (like `WSearch`) may restart automatically after reboot — this is normal Windows behavior.
- Always **create a restore point** before running aggressive optimizations.
- Use at your own risk. Tested on Windows 10 (build 17763+) and Windows 11.

---

## 🤝 Contributing

PRs are welcome! Ideas for future features:
- [ ] Restore/undo all changes button
- [ ] Startup programs manager
- [ ] GPU temperature monitoring
- [ ] Auto-boost on game launch detection
- [ ] Scheduled cleanup tasks

---

<div align="center">
  Made with 💚 for potato PC owners everywhere
  <br>
  <sub>If this saved your FPS, drop a ⭐</sub>
</div>
