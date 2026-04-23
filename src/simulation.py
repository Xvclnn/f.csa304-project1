import numpy as np

def calc_density(h, constant_density):
    """Агаарын нягтыг тооцоолох."""
    if constant_density == True:
        return 1.2
    return 1.225 * np.exp(-h / 8500.0)

def get_drag_params(t, t_shuher_zadrah):
    """Хугацаанаас хамаарч шүхрийн параметрүүдийг буцаах."""
    '''
    Энэхүү огцом шүхэр дэлгэх үед үүсэж буй агаарын эсэргүүцэл нь их хэмжээний хугацааны
    алхамтай үед Euler арга дээр алдаа үүсгэж буй тул дараах байдлаар шийдэв. 
    A болон C хоёр хувьсагчдийн шилжилтийг бага багаар нэмсэнээр бодит байдал дээрх 
    мэт шүхэр нээж буй байдалтай ойртож чадна.
    '''
    if t < t_shuher_zadrah:
        return 0.7, 0.5  # C, A (Шүхэр дэлгээгүй)
    
    shuher_neegdeh_time = 3.0
    if t < t_shuher_zadrah + shuher_neegdeh_time: 
        uurclult = (t - t_shuher_zadrah)/shuher_neegdeh_time
        C = 0.7 + uurclult * (1.5-0.7)
        A = 0.5 + uurclult * (30.0-0.5)
        return C, A
    
    return 1.5, 30.0

    

def newton_2nd(v, h, t, m, t_shuher_zadrah, constant_density):
    """Хурд болон өндрийн уламжлалыг тооцоолох."""
    g = 9.81
    C, A = get_drag_params(t, t_shuher_zadrah)
    D = calc_density(h, constant_density)
    
    hurdatgal = g - (0.5 * C * D * A * v * abs(v)) / m
    dh_dt = -v
    return hurdatgal, dh_dt

def simulate_jump(m, h0, t_shuher_zadrah, dt, method, constant_density):
    max_steps = int(2000 / dt) # array deed hemjee? 
    t = np.zeros(max_steps) # hugatsani uurclult
    v = np.zeros(max_steps) # hurdiin uurclult
    h = np.zeros(max_steps) # undriin uurclult
    
    h[0] = h0  # anhnii undur
    v[0] = 0.0 # anhnii hurd  ugasa 0
    
    for i in range(max_steps - 1):

        if method == 'euler':
            hurdatgal, dh = newton_2nd(v[i], h[i], t[i], m, t_shuher_zadrah, constant_density)
            v[i+1] = v[i] + hurdatgal * dt
            h[i+1] = h[i] + dh * dt
            
        elif method == 'rk4':
            hurdatgal1, dh1 = newton_2nd(v[i], h[i], t[i], m, t_shuher_zadrah, constant_density)
            
            v_half1 = v[i] + 0.5 * hurdatgal1 * dt
            h_half1 = h[i] + 0.5 * dh1 * dt
            hurdatgal2, dh2 = newton_2nd(v_half1, h_half1, t[i] + 0.5 * dt, m, t_shuher_zadrah, constant_density)
            
            v_half2 = v[i] + 0.5 * hurdatgal2 * dt
            h_half2 = h[i] + 0.5 * dh2 * dt
            hurdatgal3, dh3 = newton_2nd(v_half2, h_half2, t[i] + 0.5 * dt, m, t_shuher_zadrah, constant_density)
            
            v_full = v[i] + hurdatgal3 * dt
            h_full = h[i] + dh3 * dt
            hurdatgal4, dh4 = newton_2nd(v_full, h_full, t[i] + dt, m, t_shuher_zadrah, constant_density)
            
            v[i+1] = v[i] + (dt / 6.0) * (hurdatgal1 + 2*hurdatgal2 + 2*hurdatgal3 + hurdatgal4)
            h[i+1] = h[i] + (dt / 6.0) * (dh1 + 2*dh2 + 2*dh3 + dh4)
            
        t[i+1] = t[i] + dt

        # Хэрэв саяхан (h[i]) дээр тооцолсон тооцооны дараагын алхам нь газарт хүрэхээр байвал
        if h[i+1] <= 0: 
            alpha = h[i]/(h[i]-h[i+1])
            t_land = t[i] + alpha*dt
            v_land = v[i] + alpha*(v[i+1] - v[i])

            t[i+1] = t_land
            v[i+1] = v_land
            h[i+1] = 0.0

            return t[:i+2], v[:i+2], h[:i+2]        
    return t, v, h