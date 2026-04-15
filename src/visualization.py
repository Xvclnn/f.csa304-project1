import matplotlib.pyplot as plt
import numpy as np
from simulation import simulate_jump

def plot_base_simulation():
    """Үндсэн симуляцын хурд болон өндрийн хугацаанаас хамаарсан график."""
    t, v, h = simulate_jump(dt=0.1)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(t, v, 'b-', label='Хурд (м/с)')
    ax1.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    ax1.set_title('Аврагчийн унах хурд')
    ax1.set_xlabel('Хугацаа (с)')
    ax1.set_ylabel('Хурд (м/с)')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(t, h, 'g-', label='Өндөр (м)')
    ax2.axvline(x=60, color='r', linestyle='--', label='Шүхэр задрах агшин')
    ax2.set_title('Аврагчийн өндрийн өөрчлөлт')
    ax2.set_xlabel('Хугацаа (с)')
    ax2.set_ylabel('Өндөр (м)')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def plot_mass_analysis():
    """Төрөл бүрийн масстай үеийн буух хурдыг харьцуулах."""
    masses = [60, 70, 80, 90, 100]
    
    plt.figure(figsize=(10, 6))
    for m in masses:
        t, v, h = simulate_jump(m=m)
        plt.plot(t, v, label=f'm={m} кг')
        
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