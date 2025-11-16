```

  _____    ______ _    _ _____ 
 |_   _|   | ___ \ |  | /  ___|
   | | __ _| |_/ / |  | \ `--. 
   | |/ _` |    /| |/\| |`--. \
   | | (_| | |\ \\  /\  /\__/ /
   \_/\__,_\_| \_|\/  \/\____/ 

```

# TaRWS  
**Temperature & RPM Monitoring System**

TaRWS is a CPU temperature & fan RPM monitoring tool written in Python.  
It supports **three modes**:  

- **Matplotlib GUI** (default)  
- **ASCII TUI graph mode**  
- **No-Graphics logging mode**

The program collects system sensor data and generates a `log.txt` file automatically on exit.

---

## 🚀 Features

- ✔ CPU temperature monitoring  
- ✔ Fan RPM monitoring (if available)  
- ✔ **ASCII graph mode** for terminal users  
- ✔ **No-graphics mode** (silent logging mode)  
- ✔ Automatic `log.txt` generation  
- ✔ Real-time Matplotlib graph  
- ✔ Adjustable update interval  
- ✔ ASCII smoothing filter  
- ✔ Clean exit (CTRL + C)

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/javav12/TaRWS
cd TaRWS

2. Install dependencies

pip install -r requirements.txt

Or manually install:

psutil
matplotlib

🖥️ Usage
▶ Run with default Matplotlib GUI

python TaRWS.py

Shows real-time CPU temp & RPM graph.
🟩 ASCII Mode (Terminal Graph)

python TaRWS.py --ASCII_Graphics

Options:

--interval N      Data refresh interval (seconds)
--smooth N        ASCII smoothing window size

Example:
python TaRWS.py --ASCII_Graphics --interval 0.5 --smooth 3

⚪ No Graphics Mode (Just Logging)

python TaRWS.py --No_Graphics

Runs silently, displays basic values and writes log on exit.
📄 Log File

On exit, the program automatically creates:

log.txt

Format:

time,temp,rpm
0.0,45.0,1000
1.0,46.0,1020
...

⚙ Command Line Arguments
Argument Description
--No_Graphics Disable all graphics, only print values + log
--ASCII_Graphics Enable ASCII graph mode
--interval N Set data polling frequency (seconds)
--smooth N ASCII graph smoothing window
📌 Notes

    Fan RPM will show N/A on systems without fan sensors (Intel iGPU, passive cooling, etc.)

    Linux requires proper sensor drivers (lm-sensors).


🐄 Made by Cows for Everyone

TaRWS is a lightweight, simple monitoring tool designed to run anywhere.