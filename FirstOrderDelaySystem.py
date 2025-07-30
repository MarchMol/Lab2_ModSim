import numpy as np
import matplotlib.pyplot as plt

class FirstOrderDelaySystem:
    def __init__(self, initial_stock=0, initial_input=10, delay=5, dt=1):
        self.initial_stock = initial_stock
        self.initial_input = initial_input
        self.delay = delay
        self.dt = dt
        self.reset()

    def reset(self):
        self.time = []
        self.stock = []
        self.output = []
        self.input = []

    def simulate(self, total_days, input_change_day=None, new_input=None):
        stock = self.initial_stock
        input_rate = self.initial_input
        for t in range(0, total_days + 1):
            if input_change_day is not None and t >= input_change_day:
                input_rate = new_input

            outflow = stock / self.delay
            stock += self.dt * (input_rate - outflow)

            self.time.append(t)
            self.stock.append(stock)
            self.output.append(outflow)
            self.input.append(input_rate)

    def plot(self):
        eq1 = self.initial_input * self.delay
        eq2 = self.input[-1] * self.delay if self.input[-1] != self.initial_input else None

        plt.figure(figsize=(10, 6))
        plt.plot(self.time, self.stock, label='Stock', linewidth=2)
        plt.plot(self.time, self.output, label='Salida (Stock/Retardo)', linestyle='--', linewidth=2)
        plt.axhline(eq1, color='green', linestyle=':', label=f'Equilibrio 1 ({eq1} unidades)')
        if eq2 is not None:
            plt.axhline(eq2, color='red', linestyle=':', label=f'Equilibrio 2 ({eq2} unidades)')
        if eq2 is not None:
            plt.axvline(self.time[self.input.index(eq2 // self.delay)], color='gray', linestyle='--', label='Cambio en entrada')
        plt.xlabel('Tiempo (días)')
        plt.ylabel('Unidades')
        plt.title('Simulación de Retardo de Primer Orden')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Crear y simular el sistema
sistema = FirstOrderDelaySystem(initial_stock=0, initial_input=10, delay=5)
sistema.simulate(total_days=50, input_change_day=25, new_input=20)
sistema.plot()
