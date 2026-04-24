import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis import calc_terminal_velocity, is_safe_landing, calc_required_parachute_area

# ─────────────────────────────────────────────────────────────────────────────
# analysis.py  →  calc_terminal_velocity
# ─────────────────────────────────────────────────────────────────────────────

def test_positive_result():
    v = calc_terminal_velocity(m=85.0, C=0.7, A=0.5, rho=1.2)
    assert v > 0.0

def test_heavier_mass_higher_terminal_velocity():
    v1 = calc_terminal_velocity(m=70.0,  C=0.7, A=0.5, rho=1.2)
    v2 = calc_terminal_velocity(m=100.0, C=0.7, A=0.5, rho=1.2)
    assert v2 > v1

def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        calc_terminal_velocity(m=-1.0, C=0.7, A=0.5, rho=1.2)

# ─────────────────────────────────────────────────────────────────────────────
# analysis.py  →  is_safe_landing
# ─────────────────────────────────────────────────────────────────────────────

def test_slow_speed_is_safe():
    assert is_safe_landing(3.0) is True

def test_fast_speed_is_unsafe():
    assert is_safe_landing(10.0) is False

def test_negative_speed_treated_as_abs():
    assert is_safe_landing(-3.0) is True
    assert is_safe_landing(-10.0) is False

# ─────────────────────────────────────────────────────────────────────────────
# analysis.py  →  calc_required_parachute_area
# ─────────────────────────────────────────────────────────────────────────────

def test_returns_positive_area():
    area = calc_required_parachute_area(m=85.0, C=1.5, rho=1.2)
    assert area > 0.0

def test_heavier_person_needs_larger_area():
    a1 = calc_required_parachute_area(m=70.0, C=1.5, rho=1.2)
    a2 = calc_required_parachute_area(m=100.0, C=1.5, rho=1.2)
    assert a2 > a1