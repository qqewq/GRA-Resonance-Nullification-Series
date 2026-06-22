import numpy as np

class GRA_ActiveDamper:
    def __init__(self, Kp=10.0, Kd=2.0):
        self.Kp = Kp
        self.Kd = Kd
    def control_force(self, x, dx, t):
        return -self.Kp * x - self.Kd * dx

class GRA_DelayResonator:
    def __init__(self, alpha=1.0, tau=0.1):
        self.alpha = alpha
        self.tau = tau
        self.history = []   # list of (time, value)
    def control_force(self, x, t):
        self.history.append((t, x))
        # Оставляем только недавнюю историю
        self.history = [(ti, val) for ti, val in self.history if t - ti <= self.tau*2]
        target_t = t - self.tau
        if target_t < self.history[0][0]:
            return 0.0
        # Простейшая интерполяция (для тестов берём ближайшее)
        idx = np.argmin([abs(ti - target_t) for ti, _ in self.history])
        return self.alpha * self.history[idx][1]

class GRA_Metamaterial:
    def __init__(self, mc=0.1, kc=10.0):
        self.mc = mc
        self.kc = kc
    def effective_stiffness(self, omega):
        # хостовая жёсткость k_h = 100.0 для примера
        k_h = 100.0
        return k_h + self.kc**2 / (-self.mc * omega**2 + self.kc)

# Заглушка для использования в примерах
def second_order_system(m, c, k, F, x0, dx0, t):
    pass

def compute_lri(h_hist):
    T, d = h_hist.shape
    lri = np.zeros(T-1)
    for t in range(T-1):
        norm_prod = np.linalg.norm(h_hist[t]) * np.linalg.norm(h_hist[t+1])
        if norm_prod < 1e-12:
            cos_sim = 1.0
        else:
            cos_sim = np.dot(h_hist[t], h_hist[t+1]) / norm_prod
        lri[t] = 1.0 - cos_sim
    return lri

class GRA_LatentController:
    def __init__(self, Kp, Kd, target):
        self.Kp = Kp
        self.Kd = Kd
        self.target = target
        self.prev_h = target
    def control_force(self, h):
        u = -self.Kp @ (h - self.target) - self.Kd @ (h - self.prev_h)
        self.prev_h = h
        return u

def latent_dynamics(J, h0, T, noise_std, controller=None):
    d = len(h0)
    h = h0.copy()
    hist = np.zeros((T, d))
    for t in range(T):
        hist[t] = h
        u = np.zeros(d) if controller is None else controller.control_force(h)
        h = J @ h + u + noise_std * np.random.randn(d)
    return hist

class ChiralPair:
    def __init__(self, gain=0.1):
        self.gain = gain
    def step(self, state_p, state_m):
        # Взаимное притяжение с противоположным знаком
        diff = state_p + state_m
        new_p = state_p - self.gain * diff
        new_m = state_m - self.gain * diff
        return new_p, new_m
