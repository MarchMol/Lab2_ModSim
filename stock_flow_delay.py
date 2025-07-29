import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class System():
    def __init__(self, objective, s0, perception_delay, dt=1):
        self.objective = objective
        self.s0 = s0
        self.stock = s0
        
        self.perception_delay = perception_delay
        
        self.t = 0
        self.dt = dt
        self.history = []
        self.perceived = []
    
    def get_perceived(self):
        if len(self.history)>self.perception_delay:
            kernel = np.ones(self.perception_delay)/self.perception_delay
            perceived =  np.convolve(self.history, kernel, mode='same')
            return perceived[-self.perception_delay]
        else:
            return self.s0
    def step(self):
        flow = (self.objective - self.get_perceived())/self.perception_delay
        self.t += self.dt
        self.stock+= flow+self.dt
        self.history.append(self.stock)
    
    def sim(self, t_end):
        while(self.t < t_end):
            self.step()
    
    def reset(self):
        self.stock = self.s0
        self.t = 0
        self.history = []
    
    def plot(self):
        formatted = [{"t": i*self.dt, "stock": v} for i, v in enumerate(self.history)]
        df = pd.DataFrame(formatted)
        plt.plot(df["t"], df["stock"])
        
        

model = System(
    objective=50,
    s0 = 0,
    perception_delay = 15
)
for s in [0,20,30, 40,50, 60, 80,100]:
    model.s0 = s
    model.reset()
    model.sim(200)
    model.plot()
plt.show()
