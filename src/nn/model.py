import json
import numpy as np


class Model():
    def __init__(self, path=""):
        self.init_layers()

    def init_layers(self):
        self.W = np.random.standard_normal((2, 1600)) / 40
        self.b = np.random.standard_normal((2, 1))
        
    def load_model(self):
        pass

    def sigmoid(self, x):
        # print(f"DEBUG: x.shape {x.shape}")
        z = np.exp(-x)
        # print(f"DEBUG: z.shape {z.shape}")
        sig = 1 / (1 + z)
        # print(f"DEBUG: sig.shape {sig.shape}")

        return sig    

    def forward(self, input):
        net_sum = np.dot(self.W, input.T)
        # print(f"DEBUG: net_sum.shape {net_sum.shape}")
        biased = net_sum + self.b
        pred = self.sigmoid(biased)
        # print(f"DEBUG: pred.shape {pred.shape}")
        return pred.T    

    def compute_loss(self, pred, targets):
        return np.sum(-np.sum(targets * np.log(pred)) - (1 - targets) * np.log(1 - pred))

    def find_gradient(self, input, pred, target):
        # net = np.dot(W, input) + b 
        dnetdw = input

        # out = sigmoid(net)        
        doutdnet = pred * (1 - pred)
        dlossdout = pred - target

        # print(f"DEBUG: doutdnet.shape {doutdnet.shape} dlossdout.shape {dlossdout.shape}\
        #      \ndnetdw.shape {dnetdw.shape}")

        dlossdnet = dlossdout * doutdnet     
        # print(f"DEBUG: dlossdnet.shape {dlossdnet.shape}")

        dlossdw = dlossdnet.T * dnetdw
        dlossdb = dlossdnet.T 
        # print(f"DEBUG: dlossdw.shape {dlossdw.shape} dlossdb.shape {dlossdb.shape}")
        return dlossdw, dlossdb


    def step(self, learning_rate, dw, db):
        # print(f"DEBUG: before step W.shape {self.W}")
        # gradient descent
        self.W = self.W - learning_rate * dw
        self.b = self.b - learning_rate * db 

    def save_model(self, save_path):
        f = open(save_path, "w")
        model_description = dict()
        model_description["W"] = (self.W.copy()).tolist()
        model_description["b"] = (self.b.copy()).tolist()
        f.write(json.dumps(model_description))
        f.close()
        