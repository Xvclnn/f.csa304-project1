# tests/test_analysis.py
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Үндсэн модулиудаа оруулж ирэх
from src.analysis import calc_terminal_velocity, is_safe_landing

def test_is_safe_landing():
    """Газардах хурд 6 м/с-ээс бага байвал аюулгүй гэж үзнэ."""
    assert is_safe_landing(5.5) == True
    assert is_safe_landing(6.5) == False

def test_terminal_velocity_calculation():
    """Шүхэртэй үеийн тогтмол хурд ойролцоогоор 5-6 м/с орчим гарах ёстой."""
    # m=85kg, C=1.5, A=30m^2, далайн төвшний нягт D=1.225
    vt = calc_terminal_velocity(m=85.0, C=1.5, A=30.0, h=0.0)
    assert 5.0 < vt < 6.0