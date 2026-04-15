import numpy as np
from simulation import calc_density

def calc_terminal_velocity(m, C, A, h, constant_density=False):
    """Тогтмол хурдыг (terminal velocity) онолын дагуу тооцоолох."""
    g = 9.81
    D = calc_density(h, constant_density)
    return np.sqrt((2 * m * g) / (C * D * A))

def is_safe_landing(v_landing):
    """Буух үеийн хурд аюулгүй (6 м/с-ээс бага) эсэхийг шалгах."""
    return v_landing < 6.0

def find_safe_parachute_area(m=85.0, h_landing=0.0):
    """Аюулгүй буухад шаардлагатай хамгийн бага шүхрийн талбайг олох."""
    g = 9.81
    C = 1.5
    D = calc_density(h_landing)
    v_target = 5.99
    
    A_safe = (2 * m * g) / (C * D * (v_target**2))
    return A_safe