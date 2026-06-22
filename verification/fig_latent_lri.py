import numpy as np, matplotlib.pyplot as plt, sys, os
sys.path.append('../')
from gra_core import compute_lri, GRA_LatentController, latent_dynamics

d = 4
J = np.array([[0.9,0.3,0,0],[-0.3,0.9,0,0],[0,0,0.95,0.2],[0,0,-0.2,0.95]])
h0 = np.random.randn(d)
T = 200
noise_std = 0.05
ctrl = GRA_LatentController(Kp=0.3*np.eye(d), Kd=0.1*np.eye(d), target=np.zeros(d))
hist_open = latent_dynamics(J, h0, T, noise_std, controller=None)
hist_cl = latent_dynamics(J, h0, T, noise_std, controller=ctrl)
lri_open = compute_lri(hist_open)
lri_cl = compute_lri(hist_cl)
plt.figure(figsize=(8,4))
plt.plot(lri_open, 'r', label='Без GRA'); plt.plot(lri_cl, 'b', label='С GRA')
plt.xlabel('Шаг'); plt.ylabel('LRI'); plt.legend(); plt.grid(True)
plt.title('Логический резонансный индекс')
plt.tight_layout()
os.makedirs('../figures', exist_ok=True)
plt.savefig('../figures/fig_lri.png', dpi=150)
plt.close()
print('fig_lri.png сохранён')
