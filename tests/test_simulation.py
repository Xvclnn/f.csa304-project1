import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation import (
    calc_density,
    get_drag_params,
    newton_2nd,
    simulate_jump,
)



# calc_density

def test_calc_density_constant_density_returns_1_2():
    assert calc_density(0.0, True) == pytest.approx(1.2)


def test_calc_density_variable_density_at_sea_level():
    assert calc_density(0.0, False) == pytest.approx(1.225)


def test_calc_density_decreases_with_altitude():
    low = calc_density(0.0, False)
    high = calc_density(5000.0, False)

    assert high < low


def test_calc_density_matches_exponential_formula():
    h = 8500.0
    expected = 1.225 * np.exp(-h / 8500.0)

    assert calc_density(h, False) == pytest.approx(expected)


def test_calc_density_negative_altitude_gives_higher_than_sea_level_density():
    below_sea = calc_density(-100.0, False)
    sea = calc_density(0.0, False)

    assert below_sea > sea



# get_drag_params - 5 tests

def test_get_drag_params_before_parachute_opens():
    C, A = get_drag_params(4.9, 5.0)
    assert (C, A) == pytest.approx((0.7, 0.5))


def test_get_drag_params_at_exact_open_time():
    C, A = get_drag_params(5.0, 5.0)

    assert C >= 0.7 and C <= 1.5
    assert A >= 0.5 and A <= 30.0


def test_get_drag_params_after_parachute_opens():
    C, A = get_drag_params(10.0, 5.0)
    assert (C, A) == pytest.approx((1.5, 30.0))


def test_get_drag_params_negative_time_is_before_open():
    C, A = get_drag_params(-1.0, 5.0)
    assert (C, A) == pytest.approx((0.7, 0.5))


def test_get_drag_params_values_are_positive():
    C, A = get_drag_params(1.0, 5.0)
    assert C > 0 and A > 0



# newton_2nd - 5 tests

def test_newton_2nd_zero_velocity_gives_g_acceleration_and_zero_height_change():
    a, dh_dt = newton_2nd(
        v=0.0,
        h=1000.0,
        t=0.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )

    assert a == pytest.approx(9.81)
    assert dh_dt == pytest.approx(0.0)


def test_newton_2nd_before_open_has_less_than_g_acceleration_for_positive_velocity():
    a, dh_dt = newton_2nd(
        v=20.0,
        h=1000.0,
        t=0.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )

    assert a < 9.81
    assert dh_dt == pytest.approx(-20.0)


def test_newton_2nd_after_open_has_more_drag_than_before_open():
    a_before, _ = newton_2nd(
        v=20.0,
        h=1000.0,
        t=1.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )
    a_after, _ = newton_2nd(
        v=20.0,
        h=1000.0,
        t=10.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )

    assert a_after < a_before


def test_newton_2nd_negative_velocity_makes_height_increase():
    a, dh_dt = newton_2nd(
        v=-10.0,
        h=1000.0,
        t=0.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )

    assert dh_dt == pytest.approx(10.0)
    assert np.isfinite(a)


def test_newton_2nd_constant_density_changes_result_at_high_altitude():
    a_variable, _ = newton_2nd(
        v=30.0,
        h=10000.0,
        t=0.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=False,
    )
    a_constant, _ = newton_2nd(
        v=30.0,
        h=10000.0,
        t=0.0,
        m=80.0,
        t_shuher_zadrah=5.0,
        constant_density=True,
    )

    assert a_variable != pytest.approx(a_constant)



# simulate_jump - 5 tests

def test_simulate_jump_starting_on_ground_returns_immediately():
    t, v, h = simulate_jump(
        m=80.0,
        h0=0.0,
        t_shuher_zadrah=5.0,
        dt=0.1,
        method="euler",
        constant_density=False,
    )

    assert h[0] == pytest.approx(0.0)
    assert v[0] == pytest.approx(0.0)
    assert h[-1] == pytest.approx(0.0)


def test_simulate_jump_euler_initial_conditions_are_correct():
    t, v, h = simulate_jump(
        m=80.0,
        h0=1000.0,
        t_shuher_zadrah=5.0,
        dt=0.1,
        method="euler",
        constant_density=False,
    )

    assert len(t) == len(v) == len(h)
    assert h[0] == pytest.approx(1000.0)
    assert v[0] == pytest.approx(0.0)


def test_simulate_jump_rk4_time_progresses():
    dt = 0.1
    t, v, h = simulate_jump(
        m=80.0,
        h0=1000.0,
        t_shuher_zadrah=5.0,
        dt=dt,
        method="rk4",
        constant_density=False,
    )

    assert len(t) > 1
    assert t[1] == pytest.approx(dt)
    assert np.all(np.diff(t) >= 0)


def test_simulate_jump_rk4_eventually_lands():
    t, v, h = simulate_jump(
        m=80.0,
        h0=1000.0,
        t_shuher_zadrah=5.0,
        dt=0.1,
        method="rk4",
        constant_density=False,
    )

    assert h[-1] == pytest.approx(0.0)
    assert np.isfinite(v[-1])
    assert abs(v[-1]) < 20


def test_simulate_jump_smaller_dt_produces_more_steps_in_rk4():
    t1, v1, h1 = simulate_jump(
        m=80.0,
        h0=1000.0,
        t_shuher_zadrah=5.0,
        dt=0.5,
        method="rk4",
        constant_density=False,
    )
    t2, v2, h2 = simulate_jump(
        m=80.0,
        h0=1000.0,
        t_shuher_zadrah=5.0,
        dt=0.1,
        method="rk4",
        constant_density=False,
    )

    assert len(t2) > len(t1)