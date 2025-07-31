import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

beta = 0.3
mu = 0.1
N = 1000
R0_val = beta / mu

herd_immunity_threshold = 1 - 1 / R0_val
S_critico = N / R0_val

S0 = 990
I0 = 10
R0 = 0
y0 = [S0, I0, R0]

ti = 0
tf = 100
t_eval = np.linspace(ti, tf, 1000)

def sir_model(t, y):
  S, I, R = y

  if abs(t - 30) < 0.5:
    vacunados = 0.5 * S
    S -= vacunados
    R += vacunados
  dSdt = -beta * S * I / N
  dIdt = beta * S * I / N - mu * I
  dRdt = mu * I
  return [dSdt, dIdt, dRdt]

solve = solve_ivp(
  fun=sir_model,
  t_span=(ti, tf),
  y0=y0,
  t_eval=t_eval,
  vectorized=False
)

T = solve.t
S, I, R = solve.y

max_I = np.max(I)
t_max_I = T[np.argmax(I)]

plt.figure(figsize=(10, 6))
plt.plot(T, S, label='Susceptibles (S)', color='blue')
plt.plot(T, I, label='Infectados (I)', color='red')
plt.plot(T, R, label='Recuperados (R)', color='green')

plt.axvline(x=30, color='gray', linestyle='--', label='Vacunación (día 30)')
plt.axhline(y=S_critico, color='purple', linestyle='--', label='Umbral inmunidad de grupo')
plt.scatter(t_max_I, max_I, color='black', zorder=5)
plt.text(t_max_I, max_I + 10, f'Pico I: {max_I:.1f}', ha='center', fontsize=9)

plt.xlabel('Días')
plt.ylabel('Número de personas')
plt.title('Modelo SIR con vacunación (solve_ivp)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
