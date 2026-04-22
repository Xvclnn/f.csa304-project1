import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis import (
    calc_terminal_velocity,
    is_safe_landing,
    find_safe_parachute_area,
)


# =========================================================
# calc_terminal_velocity - 5 tests
# =========================================================

def test_calc_terminal_velocity_constant_density_exact_value():
    m = 80.0
    C = 1.5
    A = 25.0
    h = 0.0

    expected = np.sqrt((2 * m * 9.81) / (C * 1.2 * A))
    result = calc_terminal_velocity(m, C, A, h, constant_density=True)

    assert result == pytest.approx(expected)


def test_calc_terminal_velocity_higher_altitude_gives_higher_terminal_velocity():
    m = 80.0
    C = 1.5
    A = 25.0

    sea_level = calc_terminal_velocity(m, C, A, 0.0, constant_density=False)
    high_alt = calc_terminal_velocity(m, C, A, 10000.0, constant_density=False)

    assert high_alt > sea_level


def test_calc_terminal_velocity_raises_for_nonpositive_mass():
    with pytest.raises(ValueError):
        calc_terminal_velocity(0.0, 1.5, 25.0, 0.0)


def test_calc_terminal_velocity_raises_for_nonpositive_drag_coefficient():
    with pytest.raises(ValueError):
        calc_terminal_velocity(80.0, 0.0, 25.0, 0.0)


def test_calc_terminal_velocity_raises_for_nonpositive_area():
    with pytest.raises(ValueError):
        calc_terminal_velocity(80.0, 1.5, -1.0, 0.0)


# =========================================================
# is_safe_landing - 5 tests
# =========================================================

def test_is_safe_landing_returns_true_below_threshold():
    assert is_safe_landing(5.99) is True


def test_is_safe_landing_returns_false_at_threshold():
    assert is_safe_landing(6.0) is False


def test_is_safe_landing_returns_false_above_threshold():
    assert is_safe_landing(6.01) is False


def test_is_safe_landing_returns_true_for_zero_speed():
    assert is_safe_landing(0.0) is True


def test_is_safe_landing_returns_true_for_negative_speed_by_current_logic():
    # Function зөвхөн 6.0-оос бага эсэхийг шалгаж байгаа учраас
    # сөрөг утга дээр True буцаана.
    assert is_safe_landing(-1.0) is True


# =========================================================
# find_safe_parachute_area - 5 tests
# =========================================================

def test_find_safe_parachute_area_constant_density_exact_value():
    m = 85.0
    expected = (2 * m * 9.81) / (1.5 * 1.2 * (5.99 ** 2))

    result = find_safe_parachute_area(m=m, h_landing=0.0, constant_density=True)

    assert result == pytest.approx(expected)


def test_find_safe_parachute_area_raises_for_nonpositive_mass():
    with pytest.raises(ValueError):
        find_safe_parachute_area(m=0.0, h_landing=0.0, constant_density=False)


def test_find_safe_parachute_area_heavier_mass_requires_larger_area():
    area_light = find_safe_parachute_area(m=60.0, h_landing=0.0, constant_density=True)
    area_heavy = find_safe_parachute_area(m=100.0, h_landing=0.0, constant_density=True)

    assert area_heavy > area_light


def test_find_safe_parachute_area_higher_altitude_requires_larger_area_when_density_varies():
    area_sea = find_safe_parachute_area(m=85.0, h_landing=0.0, constant_density=False)
    area_high = find_safe_parachute_area(m=85.0, h_landing=3000.0, constant_density=False)

    assert area_high > area_sea


def test_find_safe_parachute_area_is_positive():
    area = find_safe_parachute_area(m=85.0, h_landing=0.0, constant_density=False)
    assert area > 0