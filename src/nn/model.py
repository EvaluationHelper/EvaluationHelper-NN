import numpy as np

class Model():
    def __init__(self, path=""):
        pass

    def init_layers(self):
        self.W = np.random.standard_normal((1600, 2)) / 40
        self.b = np.random.standard_normal((1600, 1))
        
    def load_model(self):
        pass

    def forward(self, imgs):
        pass

    def backward(self, loss):
        pass

    def update(self):
        pass

    def save_model(self):
        pass