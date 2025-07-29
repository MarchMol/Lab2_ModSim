import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
class System():
    def __init__(self, objective, s0, perception_delay, noise_level=0):
        self.objective = objective
        self.s0 = s0
        self.stock = s0
        
        self.perception_delay = perception_delay
        
        self.std = noise_level
        
        self.t = 0
        self.history = []
        self.perceived_history = []
    
    def add_noise(self, mean):
        return np.random.normal(loc=mean, scale=self.std)
    
    def get_perceived(self):
        if len(self.history)>self.perception_delay:
            kernel = np.ones(self.perception_delay)/self.perception_delay
            perceived =  np.convolve(self.history, kernel, mode='same')[-self.perception_delay]
            if self.std !=0:
                perceived = self.add_noise(perceived)
            self.perceived_history.append(perceived)
            return perceived
        else:
            perceived = self.s0
            if self.std !=0:
                perceived = self.add_noise(perceived)
            self.perceived_history.append(perceived)
            return perceived
    def step(self):
        flow = (self.objective - self.get_perceived())/self.perception_delay
        self.t += 1
        self.stock+= flow
        self.history.append(self.stock)
    

    def sim(self, t_end):
        while(self.t < t_end):
            self.step()
    
    def reset(self):
        self.stock = self.s0
        self.t = 0
        self.history = []
        self.perceived_history = []
    
    def plot(self):
        formatted = [{"t": i, "stock": v} for i, v in enumerate(self.history)]
        df = pd.DataFrame(formatted)
        df["perceived"] = self.perceived_history
        
        plt.title(f"Modelo Stock-Flow con retraso en percepcion {self.perception_delay}")
        plt.plot(df["t"], df["stock"], label = "Real")
        plt.plot(df["t"], df["perceived"], '--', label ="Perceived")
        plt.xlabel("Día")
        plt.ylabel("Stock")
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        

model = System(
    objective=50,
    s0 = 0,
    perception_delay = 15,
    noise_level=10
)
# for s in [0,20,30, 40,50, 60, 80,100]:
#     model.s0 = s
#     model.reset()
#     model.sim(200)
#     model.plot()
model.sim(200)
model.plot()

