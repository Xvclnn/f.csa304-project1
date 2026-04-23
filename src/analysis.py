import numpy as np

try:
    from src.simulation import calc_density, get_drag_params, simulate_jump
except ImportError:
    from simulation import calc_density, get_drag_params, simulate_jump


G = 9.81
SAFE_LANDING_SPEED = 6.0


def calc_terminal_velocity(m, C, A, h, constant_density=False):
    """Тухайн нөхцөл дэх онолын тогтмол хурдыг тооцоолно."""
    if m <= 0 or C <= 0 or A <= 0:
        raise ValueError("m, C, A нь эерэг байх шаардлагатай.")

    density = calc_density(h, constant_density)
    return np.sqrt((2 * m * G) / (C * density * A))


def is_safe_landing(v_landing, safe_speed=SAFE_LANDING_SPEED):
    """Буух үеийн хурд аюулгүй эсэхийг шалгана."""
    return bool(abs(v_landing) < safe_speed)


def find_safe_parachute_area(
    m=85.0,
    h_landing=0.0,
    constant_density=False,
    safe_speed=SAFE_LANDING_SPEED,
    C=1.5,
):
    """Аюулгүй буух хамгийн бага шүхрийн талбай A-г тооцоолно."""
    if m <= 0:
        raise ValueError("Масс эерэг байх шаардлагатай.")
    if safe_speed <= 0 or C <= 0:
        raise ValueError("safe_speed болон C нь эерэг байх шаардлагатай.")

    density = calc_density(h_landing, constant_density)
    return (2 * m * G) / (C * density * (safe_speed ** 2))


def _get_phase_indices(t, h, t_shuher_zadrah):
    """Шүхэр нээгдэхийн өмнөх болон дараах индексуудыг олно."""
    pre_idx = np.searchsorted(t, t_shuher_zadrah, side="left") - 1
    pre_idx = max(pre_idx, 0)

    post_idx = len(t) - 1
    post_idx = max(post_idx, 0)

    return pre_idx, post_idx


def compare_terminal_velocities(
    m=85.0,
    h0=4000.0,
    t_shuher_zadrah=60.0,
    dt=0.1,
    method="rk4",
    constant_density=False,
):
    """
    Онолын terminal velocity-г симуляцын үр дүнтэй харьцуулна.

    pre_parachute:
        Шүхэр нээгдэхээс өмнөх үеийн онолын болон симуляцын хурд
    post_parachute:
        Шүхэр бүрэн нээгдсэний дараах буултын үеийн онолын болон симуляцын хурд
    """
    t, v, h = simulate_jump(m, h0, t_shuher_zadrah, dt, method, constant_density)
    pre_idx, post_idx = _get_phase_indices(t, h, t_shuher_zadrah)

    pre_C, pre_A = get_drag_params(t[max(pre_idx, 0)], t_shuher_zadrah)
    post_C, post_A = 1.5, 30.0

    pre_theory = calc_terminal_velocity(
        m, pre_C, pre_A, h[pre_idx], constant_density
    )
    post_theory = calc_terminal_velocity(
        m, post_C, post_A, h[post_idx], constant_density
    )

    return {
        "simulation": {"t": t, "v": v, "h": h},
        "pre_parachute": {
            "time": float(t[pre_idx]),
            "height": float(h[pre_idx]),
            "theory_terminal_velocity": float(pre_theory),
            "simulation_velocity": float(v[pre_idx]),
        },
        "post_parachute": {
            "time": float(t[post_idx]),
            "height": float(h[post_idx]),
            "theory_terminal_velocity": float(post_theory),
            "simulation_velocity": float(v[post_idx]),
        },
        "landing": {
            "velocity": float(v[-1]),
            "is_safe": is_safe_landing(v[-1]),
        },
    }


def print_analysis_report(
    m=85.0,
    h0=4000.0,
    t_shuher_zadrah=60.0,
    dt=0.1,
    method="rk4",
    constant_density=False,
):
    """Theory vs practice харьцуулсан тайланг хэвлэнэ."""
    result = compare_terminal_velocities(
        m=m,
        h0=h0,
        t_shuher_zadrah=t_shuher_zadrah,
        dt=dt,
        method=method,
        constant_density=constant_density,
    )

    pre = result["pre_parachute"]
    post = result["post_parachute"]
    landing = result["landing"]
    min_area = find_safe_parachute_area(
        m=m,
        h_landing=0.0,
        constant_density=constant_density,
    )

    print("=== Theory vs Simulation Comparison ===")
    print(
        f"Before parachute opens: theory vt = {pre['theory_terminal_velocity']:.3f} m/s, "
        f"simulation v = {pre['simulation_velocity']:.3f} m/s at t = {pre['time']:.3f} s"
    )
    print(
        f"After parachute opens: theory vt = {post['theory_terminal_velocity']:.3f} m/s, "
        f"simulation v = {post['simulation_velocity']:.3f} m/s at t = {post['time']:.3f} s"
    )
    print(f"Landing velocity = {landing['velocity']:.3f} m/s")
    print(f"Safe to land? {'Yes' if landing['is_safe'] else 'No'}")
    print(f"Minimum safe parachute area A = {min_area:.3f} m^2")


if __name__ == "__main__":
    print_analysis_report()