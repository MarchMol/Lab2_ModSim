import numpy as np
import matplotlib.pyplot as plt

# Parámetros definidos por el usuario
entrada_diaria = 5
retardo_dias = 10
stock_inicial = 100
dias_simulacion = 60

# Inicialización de variables
tiempo = np.arange(0, dias_simulacion + 1)
stock = np.zeros(len(tiempo))
salida = np.zeros(len(tiempo))
stock[0] = stock_inicial

# Simulación usando integración de Euler
for t in range(1, len(tiempo)):
    salida[t-1] = stock[t-1] / retardo_dias
    stock[t] = stock[t-1] + entrada_diaria - salida[t-1]

# Último punto de salida
salida[-1] = stock[-1] / retardo_dias

# Gráfica
plt.figure(figsize=(10, 6))
plt.plot(tiempo, stock, label="Stock", linewidth=2)
plt.plot(tiempo, salida, label="Salida", linestyle="--", linewidth=2)
plt.axhline(y=50, color='gray', linestyle=':', label="Equilibrio esperado (Stock = 50)")
plt.title("Trayectoria del Stock y la Salida a lo largo del Tiempo")
plt.xlabel("Días")
plt.ylabel("Unidades")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
