import math

def calc_terminal_velocity(m, C, A, rho):
    """(c) Тогтмол хурдны онолын томьёо: v_t = sqrt(2mg / (C * rho * A))."""
    if C <= 0 or A <= 0 or rho <= 0:
        raise ValueError("Параметрүүд эерэг байх ёстой.")
    g = 9.81
    return math.sqrt((2.0 * m * g) / (C * rho * A))

def calc_required_parachute_area(m, C, rho, safe_speed=6.0):
    """(d) Аюулгүй буухад шаардлагатай шүхрийн талбайг олох: A = 2mg / (C * rho * v_safe^2)."""
    g = 9.81
    return (2.0 * m * g) / (C * rho * safe_speed**2)

def is_safe_landing(v_landing, threshold=6.0):
    """(d) Буух хурд аюулгүй хязгаарт багтаж буйг шалгах."""
    return abs(v_landing) <= threshold