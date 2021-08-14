import json
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
        return np.sum(-np.sum(targets * np.log(pred)) - (1 - targets) * np.log(1 - pred))

    def find_gradient(self, input, pred, target):
        # net = np.dot(W, input) + b 
        dnetdw = input
        dnetdb = np.ones(2)

        # out = sigmoid(net)        
        doutdnet = pred * (1 - pred)
        dlossdout = pred - target

        dlossdw = dlossdout * doutdnet * dnetdw
        dlossdb = dlossdout * doutdnet * dnetdb
        return dlossdw, dlossdb


    def step(self, learning_rate, dw, db):
        # gradient descent
        self.W = self.W - learning_rate * dw
        self.b = self.b - learning_rate * db 

    def save_model(self, save_path):
        f = open(save_path, "w")
        model_description = dict()
        model_description["W"] = self.W
        model_description["b"] = self.b
        f.write(json.dumps(model_description))
        f.close()
        