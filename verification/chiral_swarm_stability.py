import numpy as np, matplotlib.pyplot as plt, sys, os
sys.path.append('../')
from gra_core import ChiralPair

pair = ChiralPair(gain=0.1)
T = 200
states_plus = np.zeros((T,2))
states_minus = np.zeros((T,2))
sum_norm = np.zeros(T)
sp = np.array([1.0, 0.5]); sm = np.array([-0.8, 0.3])
for t in range(T):
    states_plus[t] = sp; states_minus[t] = sm
    sum_norm[t] = np.linalg.norm(sp+sm)
    sp, sm = pair.step(sp, sm)
plt.figure(); plt.plot(sum_norm)
plt.xlabel('Шаг'); plt.ylabel('||h+ + h-||')
plt.title('Сходимость суммы хиральной пары'); plt.grid(True)
plt.tight_layout()
os.makedirs('../figures', exist_ok=True)
plt.savefig('../figures/chiral_swarm.png', dpi=150)
plt.close()
print('chiral_swarm.png сохранён')
