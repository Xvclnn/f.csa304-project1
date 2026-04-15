# test_simulation.py
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simulation import calc_density

def test_air_density():
    """Агаарын нягтын функцийг тестлэх"""
    h_values = [4000, 3500, 3000]
    h_result = [0.765177548, 0.8115381659, 0.8607076903]
    
    results = []
    for h in h_values:
        results.append(calc_density(h))
    
    for result, expected in zip(results, h_result):
        assert abs(result - expected) < 0.0001