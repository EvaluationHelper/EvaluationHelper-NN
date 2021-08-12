import numpy as np

class Model():
    def __init__(self, path=""):
        pass

    def init_layers(self):
        self.W = np.random.standard_normal((2, 1600)) / 40
        self.b = np.random.standard_normal((2))
        
    def load_model(self):
        pass

    def sigmoid(self, x):

        z = np.exp(-x)
        sig = 1 / (1 + z)

        return sig    

    def forward(self, input):
        pred = self.sigmoid(np.dot(self.W * input) + self.b)
        return pred    

    def compute_loss(self, pred, targets):
        return -np.sum(targets * np.log(pred)) - (1 - targets) * np.log(1 - pred)

    def backward(self, loss):
        pass

    def step(self, learning_rate):
        pass

    def save_model(self):
        pass