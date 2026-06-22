import numpy as np
import sys
sys.path.append('../')
from gra_core import GRA_ActiveDamper

def test_sine_cancellation():
    damper = GRA_ActiveDamper(Kp=10.0, Kd=2.0)
    t = np.linspace(0, 10, 1000)
    omega = 2 * np.pi * 1.0
    x = np.sin(omega * t)
    dx = omega * np.cos(omega * t)
    forces = np.array([damper.control_force(xi, dxi, ti) 
                       for xi, dxi, ti in zip(x, dx, t)])
    corr = np.corrcoef(x, forces)[0, 1]
    assert corr < -0.95, f"Антикорреляция недостаточна: {corr:.3f}"
