# tests/test_simulation.py
import pytest
import numpy as np

# Үндсэн модулиудаа оруулж ирэх
from src.simulation import calc_density, get_drag_params, simulate_jump


def test_calc_density_sea_level():
    """Далайн төвшинд (h=0) агаарын нягт 1.225 байх ёстой."""
    density = calc_density(0)
    assert density == 1.225

def test_calc_density_constant():
    """Тогтмол нягттай үеийн параметр True үед нягт 1.2 гарах ёстой."""
    density = calc_density(4000, constant=True)
    assert density == 1.2

def test_get_drag_params_freefall():
    """60 секундээс өмнө (шүхэргүй үед) C=0.7, A=0.5 байх ёстой."""
    C, A = get_drag_params(30.0, 60.0)
    assert C == 0.7
    assert A == 0.5

def test_get_drag_params_parachute():
    """60 секундээс хойш (шүхэр задарсны дараа) C=1.5, A=30.0 байх ёстой."""
    C, A = get_drag_params(65.0, 60.0)
    assert C == 1.5
    assert A == 30.0

def test_simulate_jump_initial_conditions():
    """Симуляц эхлэхэд өндөр 4000м, хурд 0 байх ёстой."""
    t, v, h = simulate_jump(h0=4000.0)
    assert h[0] == 4000.0
    assert v[0] == 0.0

def test_simulate_jump_landing_condition():
    """Газардах үед буюу симуляц дуусахад өндөр 0 эсвэл түүнээс бага болсон байх ёстой."""
    t, v, h = simulate_jump(h0=4000.0, dt=1.0)
    assert h[-1] <= 0.0