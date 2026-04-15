import matplotlib.pyplot as plt
import numpy as np
from simulation import simulate_jump

methods = ['euler', 'rk4']
masses = [60, 70, 80, 90, 100]  #kg
initial_heights = [2000, 3000, 4000, 5000]  #meter
t_shuher_zadrahs = [50, 60, 70] #second
delta_t_s = [1.0, 0.1, 0.01] #second
constant_density_songolt = [True, False] 


def plot_base_simulation():
    """
    Үндсэн симуляцын хурд болон өндрийн хугацаанаас хамаарсан график байгуулна.
    """
    t, v, h = simulate_jump(m=86, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='euler', constant_density=False)
    
    fig, (plot1, plot2) = plt.subplots(2, 1, figsize=(10, 8))
    
    plot1.plot(t, v, 'b-', label='Хурд (м/с)')
    plot1.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot1.set_title('Унах хурдны өөрчлөлт')
    plot1.set_xlabel('Хугацаа (с)')
    plot1.set_ylabel('Хурд (м/с)')
    plot1.grid(True)
    plot1.legend()
    
    plot2.plot(t, h, 'g-', label='Өндөр (м)')
    plot2.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    plot2.set_title('ДТД Өндрийн өөрчлөлт')
    plot2.set_xlabel('Хугацаа (с)')
    plot2.set_ylabel('Өндөр (м)')
    plot2.grid(True)
    plot2.legend()
    
    plt.tight_layout()
    plt.show()

def plot_mass_analysis():
    """Төрөл бүрийн масстай үеийн буух хурдыг харьцуулах."""
    
    plt.figure(figsize=(10, 6))
    for mass in masses:
        t, v, h = simulate_jump(m=mass, h0=4000, t_shuher_zadrah=60, dt=delta_t_s[1], method='euler', constant_density=False)
        plt.plot(t, v, label=f'm={mass} кг')
        
    plt.axvline(x=60, color='k', linestyle='--', alpha=0.5)
    plt.title('Ялгаатай масстай үеийн хурдны харьцуулалт')
    plt.xlabel('Хугацаа (с)')
    plt.ylabel('Хурд (м/с)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_base_simulation()
    plot_mass_analysis()