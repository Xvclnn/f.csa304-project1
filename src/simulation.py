import numpy as np

def calc_density(h, constant=False):
    """Агаарын нягтыг тооцоолох."""
    if constant:
        return 1.2
    return 1.225 * np.exp(-h / 8500.0)

def get_drag_params(t, t_deploy):
    """Хугацаанаас хамаарч шүхрийн параметрүүдийг буцаах."""
    if t < t_deploy:
        return 0.7, 0.5  # C, A (Шүхэргүй)
    return 1.5, 30.0     # C, A (Шүхэртэй)

def newton_2nd(v, h, t, m, t_deploy, constant_density):
    """Хурд болон өндрийн уламжлалыг тооцоолох."""
    g = 9.81
    C, A = get_drag_params(t, t_deploy)
    D = calc_density(h, constant_density)
    
    dv_dt = g - (0.5 * C * D * A * v**2) / m
    dh_dt = -v
    return dv_dt, dh_dt

def simulate_jump(m=85.0, h0=4000.0, t_deploy=60.0, dt=0.1, method='euler', constant_density=False):
    """Шүхэртэй үсрэлтийг симуляц хийх үндсэн функц."""
    max_steps = int(2000 / dt)  # Газардах хүртэлх хангалттай хугацаа
    t = np.zeros(max_steps)
    v = np.zeros(max_steps)
    h = np.zeros(max_steps)
    
    h[0] = h0
    v[0] = 0.0
    
    for i in range(max_steps - 1):
        if h[i] <= 0:
            return t[:i+1], v[:i+1], h[:i+1]
            
        if method == 'euler':
            dv, dh = newton_2nd(v[i], h[i], t[i], m, t_deploy, constant_density)
            v[i+1] = v[i] + dv * dt
            h[i+1] = h[i] + dh * dt
            
        elif method == 'rk4':
            dv1, dh1 = newton_2nd(v[i], h[i], t[i], m, t_deploy, constant_density)
            
            v_half1 = v[i] + 0.5 * dv1 * dt
            h_half1 = h[i] + 0.5 * dh1 * dt
            dv2, dh2 = newton_2nd(v_half1, h_half1, t[i] + 0.5 * dt, m, t_deploy, constant_density)
            
            v_half2 = v[i] + 0.5 * dv2 * dt
            h_half2 = h[i] + 0.5 * dh2 * dt
            dv3, dh3 = newton_2nd(v_half2, h_half2, t[i] + 0.5 * dt, m, t_deploy, constant_density)
            
            v_full = v[i] + dv3 * dt
            h_full = h[i] + dh3 * dt
            dv4, dh4 = newton_2nd(v_full, h_full, t[i] + dt, m, t_deploy, constant_density)
            
            v[i+1] = v[i] + (dt / 6.0) * (dv1 + 2*dv2 + 2*dv3 + dv4)
            h[i+1] = h[i] + (dt / 6.0) * (dh1 + 2*dh2 + 2*dh3 + dh4)
            
        t[i+1] = t[i] + dt
        
    return t, v, h