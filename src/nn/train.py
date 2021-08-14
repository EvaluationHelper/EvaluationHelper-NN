import numpy as np
import time
import argparse
from model import Model
import os
from dataset import create_bin_dataloader

def train(positive_path, negative_path, batch_size, epochs, learning_rate, runs_path):
    # Model
    model = Model()
    
    # Train Loader
    train_dataloader = create_bin_dataloader(positive_path, negative_path, batch_size)

    # Training 
    for epoch in range(epochs):

        for i, (imgs, targets) in enumerate(train_dataloader): #=================== batch

            # Forward
            pred = model.forward(imgs)  # forward
            loss = model.compute_loss(pred, targets) # loss scaled by batch_size
            print(f"training loss: {loss}")
            
            # Backward
            dw, db = model.find_gradient(imgs, pred, targets)

            # Opimization
            model.step(learning_rate, dw, db)

    # save_model
    run_name = time.perf_counter()
    run_dir = os.path.join(runs_path, "run_" + str(run_name))
    os.mkdir(run_dir)
    model_path = os.path.join(run_dir, "model.json")
    model.save_model(model_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epochs", type=int, default=30, help="")
    parser.add_argument("-b", "--batch_size", type=int, default=50, help="")
    parser.add_argument("-p", "--positive_path", type=str, default="", help="")
    parser.add_argument("-n", "--negative_path", type=str, default="", help="")
    parser.add_argument("-r", "--learning_rate", type=str, default="", help="")
    parser.add_argument("-a", "--annotaion_path", type=str, default="", help="")
    parser.add_argument("--runs", type=str, default="../../data/runs", help="")
    opt = parser.parse_args()
    

    train(opt.positive_path, opt.negative_path, opt.batch_size, opt.epochs, opt.learning_rate, opt.runs)
    