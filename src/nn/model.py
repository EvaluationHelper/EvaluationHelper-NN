import json
import numpy as np
import os


class Model:
    def __init__(self, path=""):
        print("Load Model ...")
        if not path:
            self.init_layers()
        else:
            self.load_model(path)
        print("Load Model ... OK")

    def init_layers(self):
        '''
        Initialize the NN layers (weights, biases)
        '''
        self.W = np.random.standard_normal((2, 1600)) / 40
        self.b = np.random.standard_normal((2, 1))
        
    def load_model(self, model_path):
        f = open(os.path.join(model_path, "model.json"), "r")
        model_data = json.load(f)
        self.W = np.array(model_data["W"])
        self.b = np.array(model_data["b"])
        f.close()
        
    def sigmoid(self, x):
        z = np.exp(-x)
        sig = 1 / (1 + z)
        return sig    

    def forward(self, input):
        '''
        Make predicion on input using model
        Args:
            input : img of box
        Returns: 
            pred : prediction of the model
        '''
        net_sum = np.dot(self.W, input.T)
        biased = net_sum + self.b
        pred = self.sigmoid(biased)
        return pred.T    

    def compute_loss(self, pred, targets):
        '''
        Compute loss of prediction
        '''
        return np.sum(-np.sum(targets * np.log(pred)) - (1 - targets) * np.log(1 - pred))

    def find_gradient(self, input, pred, target): 
        '''
        Compute gradient of the model based on input, pred and target values
        Args:
            input : box img
            pred : crossed or not crossed
            target : ground truth
        Returns: 
            dloodw : impact of weights on loss 
            dlossdb : impact of biases on loss
        '''
        dnetdw = input

        doutdnet = pred * (1 - pred)
        dlossdout = pred - target

        dlossdnet = dlossdout * doutdnet     

        dlossdw = dlossdnet.T * dnetdw
        dlossdb = dlossdnet.T 
        return dlossdw, dlossdb

    def step(self, learning_rate, dw, db):
        '''
        Update model using gradient
        '''
        self.W = self.W - learning_rate * dw
        self.b = self.b - learning_rate * db 

    def save_model(self, save_path):
        '''
        Save current model
        '''
        f = open(save_path, "w")
        model_description = dict()
        model_description["W"] = (self.W.copy()).tolist()
        model_description["b"] = (self.b.copy()).tolist()
        f.write(json.dumps(model_description))
        f.close()
