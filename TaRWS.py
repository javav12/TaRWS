import argparse
import psutil
import time
import os
import atexit
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import shutil

temps = []
rpms = []
times = []

# ---- LOG SISTEMI ----
def save_log():
    with open("log.txt", "w") as f:
        f.write("time,temp,rpm\n")
        for t, temp, rpm in zip(times, temps, rpms):
            rpm_val = rpm if rpm is not None else "N/A"
            f.write(f"{t},{temp},{rpm_val}\n")
    print("\n[+] log.txt kaydedildi")

atexit.register(save_log)
# ----------------------

def get_data():
    # CPU Sıcaklığı
    t = psutil.sensors_temperatures()
    cpu_temp = None
    if "coretemp" in t:
        cpu_temp = t["coretemp"][0].current
    else:
        for v in t.values():
            cpu_temp = v[0].current
            break

    # Fan RPM
    f = psutil.sensors_fans()
    fan_rpm = None
    for v in f.values():
        fan_rpm = v[0].current
        break

    return cpu_temp, fan_rpm

# ---- ASCII GRAFIK ----
def draw_ascii_graph(data, width=80, height=20, smooth_window=3):
    if not data:
        return
    w = shutil.get_terminal_size((80, 20)).columns - 10
    width = min(width, w)
    data = data[-width:]

    # smoothing
    smooth_data = []
    N = smooth_window
    for i, v in enumerate(data):
        window = data[max(i-N+1,0):i+1]
        smooth_data.append(sum(window)/len(window))

    min_v = min(smooth_data)
    max_v = max(smooth_data)
    rng = max_v - min_v if max_v != min_v else 1

    canvas = [[" " for _ in range(width)] for _ in range(height)]
    for x, v in enumerate(smooth_data):
        y = int((v - min_v) / rng * (height - 1))
        canvas[height - 1 - y][x] = "█"

    sys.stdout.write("\033[H\033[J")
    for row in canvas:
        print("".join(row))
    print(f"Min={min_v:.2f}  Max={max_v:.2f}  Current={smooth_data[-1]:.2f}")

# ---- ARGPARSE ----
parser = argparse.ArgumentParser()
parser.add_argument("--nographics", action="store_true",
                    help="ASCII modunda çalıştır")
parser.add_argument("--interval", type=float, default=1.0,
                    help="Veri toplama ve ASCII güncelleme aralığı (saniye)")
parser.add_argument("--smooth", type=int, default=3,
                    help="ASCII grafikte smoothing window boyutu")
args = parser.parse_args()

# ---- ASCII MOD ----
if args.nographics:
    print(f"[ASCII MODE] CTRL+C ile çıkabilirsin... (interval={args.interval}s, smoothing={args.smooth})\n")
    start = time.time()
    while True:
        try:
            temp, rpm = get_data()
            t = time.time() - start

            times.append(t)
            temps.append(temp)
            rpms.append(rpm)

            os.system("clear")

            # CPU Sıcaklığı ASCII grafiği
            print("\033[92mCPU Sıcaklık (°C):", temp, "\033[0m")
            draw_ascii_graph(temps[-60:], width=60, height=15, smooth_window=args.smooth)

            # Fan RPM varsa ASCII grafiği
            if any(rpms):
                print("\033[94mFan RPM:\033[0m")
                draw_ascii_graph([v if v is not None else 0 for v in rpms[-60:]],
                                 width=60, height=5, smooth_window=args.smooth)

            print("\nZaman: {:.1f} sn".format(t))
            time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\nÇıkılıyor...")
            break

    exit()

# ---- MATPLOTLIB GRAFIK MODU ----
fig, ax = plt.subplots()
ax.set_xlabel("Zaman (sn)")
ax.set_ylabel("Değer")
ax.set_title("CPU Sıcaklık & Fan RPM")

cpu_line, = ax.plot([], [], color="green", marker="o", label="CPU (°C)")
rpm_line, = ax.plot([], [], color="blue", marker="x", label="Fan RPM")

def animate(i):
    temp, rpm = get_data()
    times.append(i)
    temps.append(temp)
    rpms.append(rpm)

    cpu_line.set_data(times, temps)

    # RPM varsa çiz
    if any(rpms):
        rpm_vals = [v if v is not None else 0 for v in rpms]
        rpm_line.set_data(times, rpm_vals)

    ax.relim()
    ax.autoscale_view()
    ax.legend()

ani = animation.FuncAnimation(fig, animate, interval=1000*args.interval, cache_frame_data=False)
plt.tight_layout()
plt.show()
