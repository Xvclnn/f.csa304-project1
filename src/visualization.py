import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def ensure_output_dir(output_dir: str = "docs/figures") -> str:
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def _save_plot(filepath: str):
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()


def plot_height_vs_time(t, h, filepath: str):
    plt.figure(figsize=(8, 5))
    plt.plot(t, h, linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.title("Height vs Time")
    plt.grid(True)
    _save_plot(filepath)


def plot_velocity_vs_time(t, v, filepath: str):
    plt.figure(figsize=(8, 5))
    plt.plot(t, v, linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Time")
    plt.grid(True)
    _save_plot(filepath)


def plot_velocity_compare(t1, v1, t2, v2, filepath: str):
    plt.figure(figsize=(8, 5))
    plt.plot(t1, v1, label="Euler", linewidth=2)
    plt.plot(t2, v2, label="RK4", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Euler vs RK4")
    plt.legend()
    plt.grid(True)
    _save_plot(filepath)


def plot_density_comparison(t1, v1, t2, v2, filepath: str):
    plt.figure(figsize=(8, 5))
    plt.plot(t1, v1, label="Variable Density", linewidth=2)
    plt.plot(t2, v2, label="Constant Density", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Variable Density vs Constant Density")
    plt.legend()
    plt.grid(True)
    _save_plot(filepath)


def plot_air_density(t, rho, filepath: str):
    plt.figure(figsize=(8, 5))
    plt.plot(t, rho, linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Air Density (kg/m^3)")
    plt.title("Air Density vs Time")
    plt.grid(True)
    _save_plot(filepath)


def plot_parachute_time_cases(results, filepath: str):
    plt.figure(figsize=(8, 5))
    for deploy_time, (t, h, v, rho) in results.items():
        plt.plot(t, v, label=f"{deploy_time} s", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Effect of Parachute Deployment Time")
    plt.legend()
    plt.grid(True)
    _save_plot(filepath)


def plot_mass_cases(results, filepath: str):
    plt.figure(figsize=(8, 5))
    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))
    for color, (mass, (t, h, v, rho)) in zip(colors, results.items()):
        plt.plot(t, v, label=f"{mass} kg", linewidth=2, color=color)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Effect of Mass on Velocity")
    plt.legend()
    plt.grid(True)
    _save_plot(filepath)


def plot_height_cases(results, filepath: str):
    plt.figure(figsize=(8, 5))
    colors = plt.cm.plasma(np.linspace(0, 1, len(results)))
    for color, (height, (t, h, v, rho)) in zip(colors, results.items()):
        plt.plot(t, v, label=f"{height} m", linewidth=2, color=color)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Effect of Initial Height on Velocity")
    plt.legend()
    plt.grid(True)
    _save_plot(filepath)


def plot_dt_comparison(summary, filepath: str):
    dts = [row["dt"] for row in summary]
    euler_vals = [row["euler_landing_velocity"] for row in summary]
    rk4_vals = [row["rk4_landing_velocity"] for row in summary]

    x = np.arange(len(dts))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x - width / 2, euler_vals, width=width, label="Euler")
    plt.bar(x + width / 2, rk4_vals, width=width, label="RK4")
    plt.xticks(x, [str(dt) for dt in dts])
    plt.xlabel("dt (s)")
    plt.ylabel("Landing Velocity (m/s)")
    plt.title("Euler vs RK4 for Different dt")
    plt.legend()
    plt.grid(True, axis="y")
    _save_plot(filepath)