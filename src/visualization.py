import matplotlib.pyplot as plt
import numpy as np
from simulation import simulate_jump


# Тогтмол утгууд
M = 85
H0 = 4000
T_SHUHER = 60
DT = 0.1


def plot_base_and_density_comparison():
    """(a), (b): Үндсэн загварчлал, хувьсах ба тогтмол нягтын харьцуулалт."""
    t1, v1, h1 = simulate_jump(M, H0, T_SHUHER, DT, 'rk4', False)
    t2, v2, h2 = simulate_jump(M, H0, T_SHUHER, DT, 'rk4', True)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(t1, v1, label='Хувьсах нягт')
    plt.plot(t2, v2, '--', label='Тогтмол нягт (1.2)')
    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Хурд (м/с)")
    plt.title("Хурд хугацаанаас хамаарах нь")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(t1, h1, label='Хувьсах нягт')
    plt.plot(t2, h2, '--', label='Тогтмол нягт (1.2)')
    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Өндөр (м)")
    plt.title("Өндөр хугацаанаас хамаарах нь")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def plot_parachute_timing_effect():
    """(d): Шүхэр 50, 60, 70 секундэд задрах үеийн хурдны өөрчлөлт."""
    times = [50, 60, 70]

    plt.figure(figsize=(8, 5))

    for ts in times:
        t, v, h = simulate_jump(M, H0, ts, DT, 'rk4', False)
        plt.plot(t, v, label=f'Шүхэр {ts} с-д задарсан')

    plt.axhline(y=6, color='r', linestyle='--', label='Аюулгүйн хязгаар (6 м/с)')
    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Хурд (м/с)")
    plt.title("Шүхэр задрах хугацааны хурданд үзүүлэх нөлөө")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_mass_variation():
    """(e): Массын өөрчлөлтийн шинжилгээ."""
    masses = [60, 70, 80, 90, 100]
    colors = plt.cm.viridis(np.linspace(0, 1, len(masses)))

    plt.figure(figsize=(8, 5))

    for m, c in zip(masses, colors):
        t, v, h = simulate_jump(m, H0, T_SHUHER, DT, 'rk4', False)
        plt.plot(t, v, color=c, label=f'Масс = {m} кг')

    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Хурд (м/с)")
    plt.title("Массын өөрчлөлтийн шинжилгээ")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_height_variation():
    """(e): Эхний өндрийн өөрчлөлтийн шинжилгээ."""
    heights = [2000, 3000, 4000, 5000]
    colors = plt.cm.plasma(np.linspace(0, 1, len(heights)))

    plt.figure(figsize=(8, 5))

    for h0, c in zip(heights, colors):
        t, v, h = simulate_jump(M, h0, T_SHUHER, DT, 'rk4', False)
        plt.plot(t, v, color=c, label=f'Эхний өндөр = {h0} м')

    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Хурд (м/с)")
    plt.title("Өндрийн өөрчлөлтийн шинжилгээ")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_euler_vs_rk4():
    """(f): Эйлер ба RK4 аргуудын харьцуулалт."""
    t_e, v_e, h_e = simulate_jump(M, H0, T_SHUHER, DT, 'euler', False)
    t_r, v_r, h_r = simulate_jump(M, H0, T_SHUHER, DT, 'rk4', False)

    plt.figure(figsize=(8, 5))
    plt.plot(t_e, v_e, label='Эйлерийн арга')
    plt.plot(t_r, v_r, '--', label='RK4 арга')
    plt.xlabel("Хугацаа (с)")
    plt.ylabel("Хурд (м/с)")
    plt.title("Эйлерийн арга ба RK4 аргын харьцуулалт")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("visualization.py ажиллаж эхэллээ...")
    plot_base_and_density_comparison()
    plot_parachute_timing_effect()
    plot_mass_variation()
    plot_height_variation()
    plot_euler_vs_rk4()
    print("зураглал дууслаа.")