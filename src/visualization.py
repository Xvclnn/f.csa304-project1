import matplotlib.pyplot as plt
import numpy as np
from simulation import simulate_jump

methods = ['euler', 'rk4']
masses = [60, 70, 80, 90, 100]
initial_heights = [2000, 3000, 4000, 5000]
t_shuher_zadrahs = [50, 60, 70]
delta_t_s = [1.0, 0.1, 0.01]
constant_density_songolt = [True, False] 


def plot_base_simulation():
    """
    Үндсэн симуляцын хурд болон өндрийн хугацаанаас хамаарсан график байгуулна.
    """
    t, v, h = simulate_jump(m=85, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='euler', constant_density=False)
    
    fig, (plot1, plot2) = plt.subplots(2, 1, figsize=(10, 8))

    
    plot1.plot(t, v, 'b-', label='Хурд (м/с)')
    plot1.axvline(x=t_shuher_zadrahs[1], color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot1.set_title('a. Унах хурдны өөрчлөлт')
    plot1.set_xlabel('Хугацаа (с)')
    plot1.set_ylabel('Хурд (м/с)')
    plot1.grid(True)
    plot1.legend()
    
    plot2.plot(t, h, 'g-', label='Өндөр (м)')
    plot2.axvline(x=t_shuher_zadrahs[1], color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot2.set_title('a. ДТД өндрийн өөрчлөлт')
    plot2.set_xlabel('Хугацаа (с)')
    plot2.set_ylabel('Өндөр (м)')
    plot2.grid(True)
    plot2.legend()
    
    plt.tight_layout()
    param_text = (
        f"m = 85 kg\n"
        f"h0 = 4000 m\n"
        f"dt = {delta_t_s[1]} s\n"
        f"method = euler\n"
        f"constant_density = False"
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.savefig('../output/1_base_plot.png') 
    plt.show()

def plot_base_density():
    """
    Үндсэн симуляцын хурд болон өндрийн хугацаанаас хамаарсан график байгуулна.
    """
    t, v, h = simulate_jump(m=85, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='euler', constant_density=True)
    
    fig, (plot1, plot2) = plt.subplots(2, 1, figsize=(10, 8))
    
    plot1.plot(t, v, 'b-', label='Хурд (м/с)')
    plot1.axvline(x=t_shuher_zadrahs[1], color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot1.set_title('b. Унах хурдны өөрчлөлт')
    plot1.set_xlabel('Хугацаа (с)')
    plot1.set_ylabel('Хурд (м/с)')
    plot1.grid(True)
    plot1.legend()
    
    plot2.plot(t, h, 'g-', label='Өндөр (м)')
    plot2.axvline(x=t_shuher_zadrahs[1], color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot2.set_title('b. ДТД өндрийн өөрчлөлт')
    plot2.set_xlabel('Хугацаа (с)')
    plot2.set_ylabel('Өндөр (м)')
    plot2.grid(True)
    plot2.legend()
    
    plt.tight_layout()
    param_text = (
        f"m = 85 kg\n"
        f"h0 = 4000 m\n"
        f"dt = {delta_t_s[1]} s\n"
        f"method = euler\n"
        f"constant_density = True"  
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.savefig('../output/2_density_const.png') 
    plt.show()


def plot_t_zadrah():
    """Шүхэр задрах хугацааны нөлөөг харьцуулах."""
    
    plt.figure(figsize=(10, 6))
    for t_zadrah in t_shuher_zadrahs:
        t, v, h = simulate_jump(m=85, h0=4000, t_shuher_zadrah=t_zadrah, dt=delta_t_s[2], method='euler', constant_density=False)
        plt.plot(t, v, label=f't_shuher_zadrah={t_zadrah} с')
        plt.axvline(x=t_zadrah, color='k', linestyle='--', alpha=0.5)
        
    plt.title('d. Шүхэр задрах хугацааны нөлөө')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Хурд (м/с)')
    plt.grid(True)
    plt.legend()
    param_text = (
        f"m = {masses[2]} kg\n"
        f"h0 = 4000 m\n"
        f"dt = {delta_t_s[0]} s\n"
        f"method = euler\n"
        f"constant_density = False"
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.savefig('../output/3_parachute_ylgaatai_time.png') 
    plt.show()


def plot_mass_analysis():
    """Төрөл бүрийн масстай үеийн буух хурдыг харьцуулах."""
    
    plt.figure(figsize=(10, 6))
    for mass in masses:
        t, v, h = simulate_jump(m=mass, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[2], method='euler', constant_density=False)
        plt.plot(t, h, label=f'm={mass} кг')
        
    plt.axvline(x=60, color='k', linestyle='--', alpha=0.5)
    plt.title('e. Ялгаатай масстай үеийн өндрийн өөчлөлт')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Өндөр (м)')
    plt.grid(True)
    plt.legend()
    param_text = (
        f"h0 = 4000 m\n"
        f"dt = {delta_t_s[2]} s\n"
        f"method = euler\n"
        f"constant_density = False"
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.savefig('../output/4_ylgaatai_masses.png') 
    plt.show()



def plot_height_ylgaa():
    ''' Анхны өндөр өөрчлөгдөхөд ямар ялгаа гарах талаар харуулна.'''
    plt.figure(figsize=(10, 6))
    for height in initial_heights:
        t, v, h = simulate_jump(m=85, h0=height, t_shuher_zadrah=60, dt=delta_t_s[2], method='euler', constant_density=False)
        plt.plot(t, h, label=f'h0={height} m')
    plt.axvline(x=60, color='k', linestyle='--', alpha=0.5)
    plt.title('e. Ялгаатай өндрөөс үсрэх үед')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Өндөр (м)')
    plt.grid(True)
    plt.legend()
    param_text = (
        f"m = {85} kg\n"
        f"dt = {delta_t_s[2]} s\n"
        f"method = euler\n"
        f"constant_density = False"
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.savefig('../output/5_ylgaatai_initial_height.png') 
    plt.show()
        

def rk4_vs_euler():
    """RK4 болон Euler аргын ялгааг харьцуулах."""

    fig, (plot_rk, plot_euler) = plt.subplots(2, 1, figsize=(10, 8))
    t_rk, v_rk, h_rk = simulate_jump(m=85, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='rk4', constant_density=False)
    t_euler, v_euler, h_euler = simulate_jump(m=85, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='euler', constant_density=False)

    plot_rk.plot(t_rk, v_rk, 'b-', label='Хурд (м/с)')
    plot_rk.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot_rk.set_title('Хурдны өөрчлөлт RK4')
    plot_rk.set_xlabel('Хугацаа (с)')
    plot_rk.set_ylabel('Хурд (м/с)')
    plot_rk.grid(True)
    plot_rk.legend()
    
    plot_euler.plot(t_euler, v_euler, 'g-', label='Өндөр (м)')
    plot_euler.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot_euler.set_title('Хурдны өөрчлөлт Euler')
    plot_euler.set_xlabel('Хугацаа (с)')
    plot_euler.set_ylabel('Хурд (м/с)')
    plot_euler.grid(True)
    plot_euler.legend()

    param_text = (
        f"m = {85} kg\n"
        f"h0 = 4000 m\n"
        f"dt = {delta_t_s[2]} s\n"
        f"method = euler\n"
        f"constant_density = False"
    )

    plt.text(
        0.02, 0.98,
        param_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    plt.tight_layout()
    plt.savefig('../output/6_rk_euler.png')
    plt.show()


if __name__ == "__main__":
    plot_base_simulation()
    plot_base_density()
    plot_mass_analysis()
    plot_t_zadrah()
    plot_height_ylgaa()
    rk4_vs_euler()