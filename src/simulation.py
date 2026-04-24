import numpy as np
import math

G = 9.81
RHO0 = 1.225
H_SCALE = 8500.0

def calc_density(h, constant_density=False):
    """(b) Агаарын нягтыг өндрөөс хамаарч тооцох."""
    h = max(float(h), 0.0)
    if constant_density:
        return 1.2
    return RHO0 * math.exp(-h / H_SCALE)

def get_drag_params(t, t_deploy):
    """(a) Шүхэр задрах агшинд параметрүүд өөрчлөгдөх."""
    if t < t_deploy:
        return 0.7, 0.5
    return 1.5, 30.0

def acceleration(v, h, t, m, t_deploy, constant_density=False):
    """Ньютоны 2-р хуулийн дагуух хурдатгал."""
    C, A = get_drag_params(t, t_deploy)
    rho = calc_density(h, constant_density)
    drag = (0.5 * C * rho * A * v * abs(v)) / m
    return G - drag

def euler_step(v, h, t, dt, m, t_deploy, constant_density=False):
    """Эйлерийн арга (f)."""
    a = acceleration(v, h, t, m, t_deploy, constant_density)
    v_next = v + a * dt
    h_next = h - v * dt
    return v_next, h_next, t + dt

def rk4_step(v, h, t, dt, m, t_deploy, constant_density=False):
    """Рунге-Куттын 4-р эрэмбийн арга (f)."""
    dv1 = acceleration(v, h, t, m, t_deploy, constant_density)
    dh1 = -v
    
    v2 = v + 0.5 * dv1 * dt
    h2 = h + 0.5 * dh1 * dt
    dv2 = acceleration(v2, h2, t + 0.5 * dt, m, t_deploy, constant_density)
    dh2 = -v2
    
    v3 = v + 0.5 * dv2 * dt
    h3 = h + 0.5 * dh2 * dt
    dv3 = acceleration(v3, h3, t + 0.5 * dt, m, t_deploy, constant_density)
    dh3 = -v3
    
    v4 = v + dv3 * dt
    h4 = h + dh3 * dt
    dv4 = acceleration(v4, h4, t + dt, m, t_deploy, constant_density)
    dh4 = -v4
    
    v_next = v + (dt / 6.0) * (dv1 + 2.0 * dv2 + 2.0 * dv3 + dv4)
    h_next = h + (dt / 6.0) * (dh1 + 2.0 * dh2 + 2.0 * dh3 + dh4)
    return v_next, h_next, t + dt



def simulate_jump(m=85.0, h0=4000.0, t_deploy=60.0, dt=0.1, method='rk4', constant_density=False):
    t, v, h = 0.0, 0.0, float(h0)
    t_vals, v_vals, h_vals = [t], [v], [h]
    stepper = euler_step if method == 'euler' else rk4_step

    while h > 0:
        v_next, h_next, t_next = stepper(v, h, t, dt, m, t_deploy, constant_density)
        
        if h_next <= 0.0:
            frac = h / (h - h_next)
            t = t + frac * dt
            v = v + frac * (v_next - v)
            h = 0.0
            t_vals.append(t)
            v_vals.append(v)
            h_vals.append(h)
            break
            
        v, h, t = v_next, h_next, t_next
        t_vals.append(t)
        v_vals.append(v)
        h_vals.append(h)
        
    return {
        't': np.array(t_vals),
        'v': np.array(v_vals),
        'h': np.array(h_vals),
        'landing_speed': float(v_vals[-1]),
        'landing_time': float(t_vals[-1])
    }