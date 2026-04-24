import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from simulation import simulate_jump, get_drag_params, calc_density
from analysis import calc_terminal_velocity, calc_required_parachute_area, is_safe_landing

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _savefig(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
# ==========================================
# ГРАФИК ЗУРАХ ФУНКЦҮҮД
# ==========================================

def plot_base_simulation():
    """(a) Суурь загварын хурд болон өндрийн график."""
    res = simulate_jump(dt=0.1)
    t, v, h = res['t'], res['v'], res['h']
    color = cm.viridis(0.4)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    ax1.plot(t, v, label='Хурд (м/с)', color=color, linewidth=2)
    ax1.plot(t[-1], res['landing_speed'], 'x', markersize=12, markeredgewidth=3, color='red', label='Газардсан агшин')
    ax1.axvline(60, color='gray', linestyle='--', alpha=0.6, label='Шүхэр задрах')
    ax1.set_title('Үндсэн загвар: Хурд, хугацааны график')
    ax1.set_ylabel('Хурд (м/с)')
    ax1.grid(True); ax1.legend()

    ax2.plot(t, h, label='Өндөр (м)', color=color, linewidth=2)
    ax2.plot(t[-1], 0, 'x', markersize=12, markeredgewidth=3, color='red', label='Газардсан цэг (h=0)')
    ax2.axvline(60, color='gray', linestyle='--', alpha=0.6)
    ax2.set_title('Үндсэн загвар: Өндөр, хугацааны график')
    ax2.set_ylabel('Өндөр (м)')
    ax2.set_xlabel('Хугацаа (с)')
    ax2.grid(True); ax2.legend()

    _savefig('A_simulation.png')

def plot_density_comparison():
    """(b) Хувьсах болон тогтмол нягтын харьцуулалт."""
    res_var = simulate_jump(constant_density=False)
    res_const = simulate_jump(constant_density=True)
    colors = cm.viridis([0.25, 0.75])

    plt.figure(figsize=(10, 6))
    
    plt.plot(res_var['t'], res_var['v'], color=colors[0], label='Хувьсах нягт (ρ(h))', linewidth=2)
    plt.plot(res_var['t'][-1], res_var['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[0])

    plt.plot(res_const['t'], res_const['v'], color=colors[1], label='Тогтмол нягт (1.2)', linewidth=2)
    plt.plot(res_const['t'][-1], res_const['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[1])

    plt.axvline(60, color='gray', linestyle='--', alpha=0.5)
    plt.title('Агаарын нягтын загваруудын харьцуулалт')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Хурд (м/с)')
    plt.grid(True); plt.legend()
    _savefig('A_2_comparison.png')

def plot_safety_analysis():
    """(d) Шүхэр задрах хугацааны аюулгүй байдлын нөлөө."""
    deploy_times = [50, 60, 70]
    colors = cm.viridis(np.linspace(0.1, 0.9, len(deploy_times)))

    plt.figure(figsize=(10, 6))
    for idx, t_dep in enumerate(deploy_times):
        res = simulate_jump(h0=4000, t_deploy=t_dep)
        v_land = res['landing_speed']
        
        plt.plot(res['t'], res['v'], color=colors[idx], label=f'Задрах: {t_dep} с', linewidth=2)
        plt.plot(res['t'][-1], v_land, 'x', markersize=12, markeredgewidth=2, color=colors[idx])
        plt.axvline(t_dep, color=colors[idx], linestyle='--', alpha=0.3)

    plt.axhline(6.0, color='red', linestyle=':', linewidth=2, label='Аюулгүй хязгаар (6 м/с)')
    plt.title('Шүхэр задрах хугацааны нөлөө ба аюулгүй байдал')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Хурд (м/с)')
    plt.grid(True); plt.legend()
    _savefig('D_safety_analysis.png')

def plot_mass_analysis():
    """(e) Масс 60, 70, 80, 90, 100 байх үеийн харьцуулалт."""
    masses = [60, 70, 80, 90, 100]
    colors = cm.viridis(np.linspace(0, 1, len(masses)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    for idx, m in enumerate(masses):
        res = simulate_jump(m=m)
        t, v, h = res['t'], res['v'], res['h']
        
        ax1.plot(t, v, label=f'{m} кг', color=colors[idx], linewidth=1.5)
        ax1.plot(t[-1], res['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[idx])

        ax2.plot(t, h, label=f'{m} кг', color=colors[idx], linewidth=1.5)
        ax2.plot(t[-1], 0, 'x', markersize=10, markeredgewidth=2, color=colors[idx])

    ax1.axvline(60, color='gray', linestyle='--', alpha=0.5, label='Шүхэр задрах')
    ax1.set_title('e. Биеийн массын нөлөө: Хурд')
    ax1.set_ylabel('Хурд (м/с)')
    ax1.grid(True); ax1.legend()

    ax2.axvline(60, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('e. Биеийн массын нөлөө: Өндөр')
    ax2.set_xlabel('Хугацаа (с)')
    ax2.set_ylabel('Өндөр (м)')
    ax2.grid(True); ax2.legend()

    _savefig('E_1_mass_analysis.png')

def plot_height_analysis_colormap():
    """(e) Өндрийн харьцуулалтыг colormap ашиглан зурах."""
    heights = [2000, 3000, 4000, 5000]
    colors = cm.viridis(np.linspace(0, 1, len(heights)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    for idx, h0 in enumerate(heights):
        res = simulate_jump(h0=h0)
        t, v, h = res['t'], res['v'], res['h']

        ax1.plot(t, v, color=colors[idx], label=f'Эхний өндөр: {h0} м', linewidth=1.5)
        ax1.plot(t[-1], res['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[idx])

        ax2.plot(t, h, color=colors[idx], label=f'Эхний өндөр: {h0} м', linewidth=1.5)
        ax2.plot(t[-1], 0, 'x', markersize=10, markeredgewidth=2, color=colors[idx])

    ax1.axvline(60, color='gray', linestyle='--', alpha=0.4)
    ax1.set_title('e. Үсрэлтийн өндрийн нөлөө: Хурд')
    ax1.set_ylabel('Хурд (м/с)')
    ax1.grid(True); ax1.legend()

    ax2.axvline(60, color='gray', linestyle='--', alpha=0.4)
    ax2.set_title('e. Үсрэлтийн өндрийн нөлөө: Өндөр')
    ax2.set_xlabel('Хугацаа (с)')
    ax2.set_ylabel('Өндөр (м)')
    ax2.grid(True); ax2.legend()

    _savefig('E_2_height_analysis.png')

def plot_rk4_vs_euler():
    """(f) RK4 болон Euler аргын ялгааг 3 өөр dt дээр харуулах."""
    dts = [1.0, 0.1, 0.01]
    colors = cm.viridis([0.3, 0.8]) 
    
    for dt in dts:
        res_rk4 = simulate_jump(dt=dt, method='rk4')
        res_eu  = simulate_jump(dt=dt, method='euler')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f'Аргуудын харьцуулалт: dt = {dt} с', fontsize=14, fontweight='bold')

        ax1.plot(res_rk4['t'], res_rk4['v'], label=f'RK4 (илүү нарийн)', color=colors[1], linewidth=2)
        ax1.plot(res_eu['t'], res_eu['v'], label=f'Euler (энгийн)', color=colors[0], linestyle='--', linewidth=2)
        
        ax1.plot(res_rk4['t'][-1], res_rk4['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[1])
        ax1.plot(res_eu['t'][-1], res_eu['landing_speed'], 'x', markersize=10, markeredgewidth=2, color=colors[0])
        
        ax1.set_ylabel('Хурд (м/с)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.plot(res_rk4['t'], res_rk4['v'], '-', label=f'RK4', color=colors[1], linewidth=2)
        ax2.plot(res_eu['t'], res_eu['v'], '--', label=f'Euler', color=colors[0], linewidth=2)
        
        ax2.set_xlim(58, 65)
        ax2.set_ylim(-5, 60)
        ax2.set_title('Шүхэр задрах агшны шилжилт (Zoom)', fontsize=12)
        ax2.set_ylabel('Хурд (м/с)')
        ax2.set_xlabel('Хугацаа (с)')
        ax2.axvline(60, color='red', linestyle=':', alpha=0.6, label='Шүхэр задрах цэг')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        filename = f'F_rk4_vs_euler_dt_{str(dt).replace(".", "_")}.png'
        plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)


# ==========================================
# ТЕРМИНАЛД ХЭВЛЭХ (ТАЙЛАНГИЙН) ФУНКЦҮҮД
# ==========================================

def print_terminal_velocity_check():
    """(c) Онолын тогтмол хурдыг симуляцтай харьцуулж баталгаажуулах."""
    m = 85.0
    rho = 1.2 
    
    C_free, A_free = get_drag_params(0, 60)
    C_open, A_open = get_drag_params(70, 60)
    
    vt_free = calc_terminal_velocity(m, C_free, A_free, rho)
    vt_open = calc_terminal_velocity(m, C_open, A_open, rho)
    
    res = simulate_jump(dt=0.01, constant_density=True)
    v_sim_free = max(res['v'])
    v_sim_open = res['landing_speed']
    
    print("\n" + "="*60)
    print(" (c) ТОГТМОЛ ХУРДНЫ БАТАЛГААЖУУЛАЛТ (Тогтмол нягт: 1.2)")
    print(f"Шүхэргүй үеийн онолын хурд:  {vt_free:.2f} м/с")
    print(f"Шүхэргүй үеийн симуляцийн:   {v_sim_free:.2f} м/с")
    print("-" * 60)
    print(f"Шүхэртэй үеийн онолын хурд:  {vt_open:.2f} м/с")
    print(f"Шүхэртэй үеийн симуляцийн:   {v_sim_open:.2f} м/с")

def print_safety_check():
    """(d) Аюулгүй байдлын шинжилгээ."""
    print("\n" + "="*65)
    print(" (d) АЮУЛГҮЙ БАЙДЛЫН ШИНЖИЛГЭЭ")
    
    print("1. Шүхэр 50, 60, 70 секундэд задрах үеийн шалгалт (Масс: 85 кг):")
    for t_dep in [50, 60, 70]:
        res = simulate_jump(m=85.0, h0=5000.0, t_deploy=t_dep, dt=0.01)
        v_land = res['landing_speed']
        safe = is_safe_landing(v_land, 6.0)
        safe_str = "ТИЙМ (Аюулгүй)" if safe else "ҮГҮЙ (Аюултай)"
        print(f" - Задрах хугацаа {t_dep} с: Буух хурд = {v_land:.2f} м/с | < 6 м/с эсэх: {safe_str}")


def print_rk4_vs_euler_table():
    """(f) RK4 ба Euler аргын алдааны зөрүүг хүснэгтээр харуулах."""
    print("\n" + "="*60)
    print(" (f) RK4 БОЛОН ЭЙЛЕР АРГЫН ХАРЬЦУУЛАЛТ (Буух хурдаар)")
    print("-" * 60)
    print(f"{'dt (сек)':<10} | {'Euler (м/с)':<15} | {'RK4 (м/с)':<15} | {'Зөрүү':<10}")
    print("-" * 60)
    
    for dt in [1.0, 0.1, 0.01]:
        eu = simulate_jump(dt=dt, method='euler')['landing_speed']
        rk = simulate_jump(dt=dt, method='rk4')['landing_speed']
        diff = abs(eu - rk)
        
        if eu < -1000 or eu > 1000:
            eu_str = "Сарнисан!"
            diff_str = "N/A"
        else:
            eu_str = f"{eu:.4f}"
            diff_str = f"{diff:.4f}"
            
        print(f"{dt:<10} | {eu_str:<15} | {rk:<15.4f} | {diff_str:<10}")
    print("="*60 + "\n")


if __name__ == '__main__':
    print("Графикуудыг зурж 'output/' хавтсанд хадгалж байна...")
    plot_base_simulation()
    plot_density_comparison()
    plot_safety_analysis()
    plot_mass_analysis()
    plot_height_analysis_colormap()
    plot_rk4_vs_euler()
    
    print_terminal_velocity_check()
    print_safety_check()
    print_rk4_vs_euler_table()
    
    plt.show()