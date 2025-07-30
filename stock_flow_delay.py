import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
class System():
    def __init__(self, objective, s0, perception_delay, noise_level=0):
        # Save objective and initial stock for easier resetting
        self.objective = objective
        self.s0 = s0
        self.stock = s0
        
        # Perception delay and noise level
        self.perception_delay = perception_delay
        self.std = noise_level
        
        # dt will be consider as 1 unit of time.
        self.t = 0
        
        # History of stocks and perceived stocjs
        self.history = []
        self.perceived_history = []
    
    def add_noise(self, mean):
        # Adds noise to a value given a set standard deviation
        return np.random.normal(loc=mean, scale=self.std)
    
    def get_perceived(self):
        if len(self.history)>self.perception_delay:
            # If there are sufficient values for perception delay
            
            kernel = np.ones(self.perception_delay)/self.perception_delay # linear kernel
            # From convolution, obtaining the value at the moment of perception
            perceived =  np.convolve(self.history, kernel, mode='same')[-self.perception_delay] 
            if self.std !=0:
                perceived = self.add_noise(perceived)
            self.perceived_history.append(perceived)
            return perceived
        else:
            # If there arent sufficient values for delay , just return initial value
            perceived = self.s0
            if self.std !=0:
                perceived = self.add_noise(perceived)
            self.perceived_history.append(perceived)
            return perceived
        
    def step(self):
        # Calculate flow with given equation
        flow = (self.objective - self.get_perceived())/self.perception_delay
        self.t += 1 # advance time
        self.stock+= flow # change stock accordingly
        self.history.append(self.stock) # save value
    

    def sim(self, t_end):
        while(self.t < t_end):
            self.step()
    
    def reset(self):
        self.stock = self.s0
        self.t = 0
        self.history = []
        self.perceived_history = []
        self.flow_history = []
    
    def plot(self):
        # Converting number array into labeled dataframe
        formatted = [{"t": i, "stock": v} for i, v in enumerate(self.history)]
        df = pd.DataFrame(formatted)
        # Save perceived
        df["perceived"] = self.perceived_history
        
        # Calculate overcorrection points
        deviation = df["stock"] - self.objective
        sign_change = np.diff(np.sign(deviation))
        oc_idx = np.where(sign_change!=0)[0] + 1
        
        plt.title(f"Modelo Stock-Flow con retraso en percepcion {self.perception_delay}\nObjetivo = {self.objective}, Ruido = {self.std}")
        plt.plot(df["t"], df["stock"], label = "Real")
        plt.plot(df["t"], df["perceived"], label ="Perceived", color="b", alpha = 0.2)
        
        plt.axhline(self.objective, 0, df.shape[0], linestyle=':', color='g', label="Target")
        plt.scatter(df["t"][oc_idx], df["stock"][oc_idx], label="Overcorrection", color='r')
        
        plt.xlabel("Día")
        plt.ylabel("Stock")
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        
# Exmple
model = System(
    objective=50,
    s0 = 0,
    perception_delay = 15,
    noise_level=0.2
)
model.sim(200)
model.plot()

