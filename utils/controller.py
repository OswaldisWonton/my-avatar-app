import numpy as np

def detect_no_people(T=100, threshold=0.9):
    threshold_controller = ThresholdController(T=100, threshold_high=0.9)

class ThresholdController:
    def __init__(self, T, threshold_low=0.0, threshold_high=1.0):
        self.T = T
        self.cache = np.zeros(T)
        self.p = 0
        if threshold_low is None and threshold_high is None:
            exit("[INFO] Need at least one threshold!")
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high
    
    def _set(self):
        self.cache[:] = 1
    
    def _reset(self):
        self.cache[:] = 0
    
    def __call__(self, b):
        self.cache[self.p] = b
        self.p = (self.p + 1) % self.T
        tmp = self.cache.mean()
        return (tmp >= self.threshold_low) and (tmp <= self.threshold_high)
