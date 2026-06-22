import numpy as np
from gra_core import GRA_Metamaterial

def test_antiresonance_notch():
    cell = GRA_Metamaterial(mc=0.1, kc=10.0)
    omega = np.linspace(0.1, 20, 2000)
    K = np.array([cell.effective_stiffness(w) for w in omega])
    min_idx = np.argmin(np.abs(K))
    assert np.abs(K[min_idx]) < 1e-3, f"Нет антирезонанса: min|K| = {np.abs(K[min_idx]):.5f}"
