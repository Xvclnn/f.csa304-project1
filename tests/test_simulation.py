import math
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.simulation import (
    calc_density, get_drag_params, acceleration, 
    euler_step, rk4_step, simulate_jump, RHO0, G
)

# ─────────────────────────────────────────────────────────────────────────────
# simulation.py  →  calc_density
# ─────────────────────────────────────────────────────────────────────────────

def test_sea_level_returns_rho0():
    assert calc_density(0.0) == pytest.approx(RHO0, rel=1e-9)

def test_density_decreases_with_altitude():
    assert calc_density(1000.0) < calc_density(0.0)

def test_constant_density_flag():
    assert calc_density(5000.0, constant_density=True) == pytest.approx(1.2)


# ─────────────────────────────────────────────────────────────────────────────
# simulation.py  →  get_drag_params (3 тест)
# ─────────────────────────────────────────────────────────────────────────────

def test_get_drag_params_before_deploy():
    C, A = get_drag_params(t=10.0, t_deploy=60.0)
    assert C == 0.7 and A == 0.5

def test_get_drag_params_after_deploy():
    C, A = get_drag_params(t=61.0, t_deploy=60.0)
    assert C == 1.5 and A == 30.0

def test_get_drag_params_at_exact_deploy_time():
    C, A = get_drag_params(t=60.0, t_deploy=60.0)
    assert C == 1.5 and A == 30.0

# ─────────────────────────────────────────────────────────────────────────────
# simulation.py  →  acceleration (3 тест)
# ─────────────────────────────────────────────────────────────────────────────

def test_acceleration_at_zero_velocity():
    a = acceleration(v=0.0, h=0.0, t=0.0, m=85.0, t_deploy=60.0)
    assert a == pytest.approx(G, rel=1e-9)

def test_acceleration_reduces_as_velocity_increases():
    a_slow = acceleration(v=5.0, h=0.0, t=0.0, m=85.0, t_deploy=60.0)
    a_fast = acceleration(v=20.0, h=0.0, t=0.0, m=85.0, t_deploy=60.0)
    assert a_fast < a_slow

def test_acceleration_is_lower_with_open_chute():
    a_no_chute = acceleration(v=10.0, h=0.0, t=50.0, m=85.0, t_deploy=60.0)
    a_chute    = acceleration(v=10.0, h=0.0, t=70.0, m=85.0, t_deploy=60.0)
    assert a_chute < a_no_chute

# ─────────────────────────────────────────────────────────────────────────────
# simulation.py  →  simulate_jump (3 тест)
# ─────────────────────────────────────────────────────────────────────────────

def test_simulate_jump_returns_required_keys():
    result = simulate_jump(m=85.0, h0=100.0, t_deploy=5.0, dt=0.1)
    expected_keys = {'t', 'v', 'h', 'landing_time', 'landing_speed'}
    assert expected_keys.issubset(result.keys())

def test_simulate_jump_rk4_and_euler_both_land():
    r_rk4   = simulate_jump(h0=300.0, t_deploy=10.0, dt=0.1, method='rk4')
    r_euler = simulate_jump(h0=300.0, t_deploy=10.0, dt=0.1, method='euler')
    assert r_rk4['h'][-1]   == pytest.approx(0.0, abs=1e-6)
    assert r_euler['h'][-1] == pytest.approx(0.0, abs=1e-6)

def test_simulate_jump_higher_start_takes_longer():
    res_low  = simulate_jump(h0=100.0, t_deploy=5.0)
    res_high = simulate_jump(h0=500.0, t_deploy=5.0)
    assert res_high['landing_time'] > res_low['landing_time']