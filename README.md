# ⚡ ToasterBoosterX

> **A free, open-source Windows optimizer built for low-end PCs — because everyone deserves a fast computer.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Admin](https://img.shields.io/badge/Requires-Admin-red?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-orange?style=for-the-badge)

---

## 🖥️ What is ToasterBoosterX?

ToasterBoosterX is a **real-time Windows performance optimizer** with a cyberpunk neon UI. It boosts FPS, frees up RAM, cleans junk files, kills background services, and applies system tweaks — all in one click.

Designed especially for **potato PCs and toaster laptops** that struggle to run games or apps smoothly. No bloat, no subscriptions, no BS — just raw speed.

---

## 🎨 UI Preview

```
╔══════════════════════════════════════════════╗
║   TOASTER BOOSTER X   (glitch animated)      ║
╠══════════════════════════════════════════════╣
║  [CPU ◉]  [RAM ◉]  [GPU ◉]  [DISK ◉]        ║
║   neon arc meters with smooth animation      ║
╠══════════════════════════════════════════════╣
║        ▶  BOOST SYSTEM  ◀  (pulsing)         ║
╠══════════════════════════════════════════════╣
║  [VIDEO MODE]  [STREAM MODE]  [ULTRA FPS]    ║
║  [TEMP CLEAN]  [SERVICES]  [RAM]  [DNS]      ║
╠══════════════════════════════════════════════╣
║  >> SYSTEM LOG (live output)                 ║
╚══════════════════════════════════════════════╝
```

> Dark cyberpunk aesthetic — neon green / cyan / pink / yellow on black

---

## 📥 Installation

### ✅ Option 1 — Easy (Recommended, no setup needed)

1. Go to the [**Releases**](../../releases) page
2. Download `ToasterBoosterX.zip`
3. Extract the zip to any folder
4. Double-click `ESTABLISH_AND_COMPILE.bat`
   - Automatically installs all Python dependencies
   - Builds `ToasterBoosterX.exe` for you
5. Open the `dist/` folder → run **`ToasterBoosterX.exe`**
6. Windows will ask for **Administrator** — click **Yes**

> 💡 You only need to run the `.bat` once. After that, just use the `.exe` directly.

---

### 🐍 Option 2 — Run from Source (Python users)

```bash
# 1. Clone the repo
git clone https://github.com/Ast1Kaan/ToasterBoosterX.git
cd ToasterBoosterX

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run as Administrator
python optimizer.py
```

---

### 🔨 Option 3 — Build EXE yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --uac-admin --name "ToasterBoosterX" --collect-all customtkinter --hidden-import psutil --hidden-import GPUtil optimizer.py
```

The `.exe` will appear in `dist/`. No Python needed on the target machine — send it to anyone.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚀 **One-Click BOOST** | Applies all optimizations at once |
| 📊 **Live Hardware Meters** | Real-time CPU / RAM / GPU / DISK monitoring with animated neon arcs |
| 🗑️ **Temp Cleaner** | Clears Windows temp folders and shows how many MB were freed |
| 🔧 **Service Killer** | Stops FPS-tanking background Windows services |
| 💾 **RAM Flush** | Forces working set cleanup across all running processes |
| 🌐 **DNS Flush** | Clears DNS cache for faster browsing and lower ping |
| 🎮 **Ultra FPS Mode** | Max performance power plan + all registry tweaks applied |
| 📹 **Video Capture Mode** | Balanced power plan optimized for recording |
| 🎮 **Game + Stream Mode** | High performance plan for gaming and streaming simultaneously |
| 🖱️ **Mouse Acceleration OFF** | Disables Windows mouse acceleration for raw, precise aim |
| 🎯 **GPU Hardware Scheduling** | Enables HAGS for better GPU frame delivery |
| 🏆 **MMCSS Game Priority** | Sets HIGH scheduling priority for games via registry |
| 🌍 **TCP Network Tweaks** | Optimizes TCP auto-tuning and ECN for better connection |

---

## ⚙️ What Does BOOST Actually Do?

When you hit the **BOOST** button, the following runs automatically in order:

1. Switches power plan to **Ultimate Performance**
2. Runs Python garbage collector (`gc.collect()`)
3. Clears all **Temp folders**:
   - `%TEMP%`, `C:\Windows\Temp`, `C:\Windows\Prefetch`, `%LOCALAPPDATA%\Temp`
4. Stops background **Windows services** that eat FPS:
   - `SysMain` (Superfetch), `WSearch`, `XboxNetApiSvc`, `XblGameSave`, `XblAuthManager`, `Fax`, `DiagTrack`, `dmwappushservice`
5. **Flushes RAM** — cleans working sets across all processes via PowerShell
6. **Flushes DNS** cache (`ipconfig /flushdns`)
7. Applies **registry tweaks**:
   - Mouse acceleration OFF
   - Hardware-Accelerated GPU Scheduling (HAGS) ON
   - Game Bar auto-mode ON
   - MMCSS game scheduling priority HIGH
   - TCP auto-tuning + ECN enabled

---

## 📦 Requirements

| Package | Version |
|---|---|
| customtkinter | 5.2.2 |
| psutil | 5.9.8 |
| GPUtil | 1.4.0 |
| Pillow | 10.3.0 |
| pyinstaller | 6.6.0 *(build only)* |

```bash
pip install -r requirements.txt
```

---

## ❓ FAQ

**Q: Do I need Python installed to use this?**
No. If you use the `.exe` from Releases, Python is not required. It is fully self-contained.

**Q: Will this break my PC?**
It stops some non-essential Windows services and writes a few registry values. Nothing destructive. Services restart automatically on reboot if Windows needs them.

**Q: Why does my antivirus flag it?**
Because it uses pyinstaller, modifies registry, and runs as admin. This is a false positive — the source code is fully open and auditable right here.

**Q: The services restart after reboot — is that normal?**
Yes. Windows restarts services like WSearch automatically. Run BOOST again after booting if you want them stopped.

**Q: Does it work on Windows 11?**
Yes. Tested on Windows 10 (build 17763+) and Windows 11.

---

## ⚠️ Disclaimer

- This tool modifies **Windows registry** and **stops system services.**
- Always **create a restore point** before running aggressive optimizations.
- Use at your own risk. The developer is not responsible for any damage.

---

## 🤝 Contributing

PRs are welcome! Ideas for future features:
- [ ] Restore / undo all changes button
- [ ] Startup programs manager
- [ ] GPU temperature monitoring
- [ ] Auto-boost on game launch detection
- [ ] Scheduled cleanup tasks
- [ ] Multi-language support

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Made with 💚 for potato PC owners everywhere

**[⭐ Star this repo if it helped your FPS](../../stargazers)**  &nbsp;·&nbsp;  **[🐛 Report a bug](../../issues)**  &nbsp;·&nbsp;  **[💡 Request a feature](../../issues)**

</div>
