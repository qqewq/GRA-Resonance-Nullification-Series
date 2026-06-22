import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append('../')
from gra_core import GRA_ActiveDamper

m, c, k = 1.0, 0.1, 100.0
omega0 = np.sqrt(k/m)
freqs = np.linspace(0.5*omega0, 2*omega0, 500)
amp_open, amp_cl = [], []
damper = GRA_ActiveDamper(Kp=30.0, Kd=2.0)
for w in freqs:
    amp_open.append(1/np.sqrt((k - m*w**2)**2 + (c*w)**2))
    amp_cl.append(1/np.sqrt((k+damper.Kp - m*w**2)**2 + ((c+damper.Kd)*w)**2))
plt.figure(figsize=(8,5))
plt.semilogy(freqs, amp_open, 'r', label='Без GRA')
plt.semilogy(freqs, amp_cl, 'b', label='С GRA')
plt.xlabel('Частота, рад/с'); plt.ylabel('Амплитуда')
plt.legend(); plt.grid(True, which='both', ls='--')
plt.title('Подавление резонанса активным GRA-демпфером')
plt.tight_layout()
os.makedirs('../figures', exist_ok=True)
plt.savefig('../figures/fig1.png', dpi=150)
plt.close()
print('fig1.png сохранён')
