import numpy as np
from gra_core import GRA_DelayResonator

def test_delay_half_period():
    omega = 2 * np.pi * 5.0
    tau = np.pi / omega
    resonator = GRA_DelayResonator(alpha=1.0, tau=tau)
    t = np.linspace(0, 1, 2000)
    x = np.sin(omega * t)
    y = np.array([resonator.control_force(xi, ti) for xi, ti in zip(x, t)])
    # Пропускаем переходной участок
    start = int(tau / (t[1]-t[0])) + 10
    corr = np.corrcoef(x[:-start], y[start:])[0, 1]
    assert corr < -0.9, f"Ожидалась отрицательная корреляция, получено {corr:.3f}"
