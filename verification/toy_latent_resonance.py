import numpy as np, sys
sys.path.append('../')
from gra_core import GRA_LatentController, latent_dynamics, compute_lri

theta = np.pi/6
J = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]]) * 0.99
ctrl = GRA_LatentController(Kp=0.4*np.eye(2), Kd=0.2*np.eye(2), target=np.zeros(2))
h0 = np.array([1.0, 0.0])
h_open = latent_dynamics(J, h0, 100, 0.0, None)
h_cl = latent_dynamics(J, h0, 100, 0.0, ctrl)
print(f"Без GRA: LRI среднее = {compute_lri(h_open).mean():.4f}")
print(f"С GRA:   LRI среднее = {compute_lri(h_cl).mean():.4f}")
