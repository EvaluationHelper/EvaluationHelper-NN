import numpy as np
import time
import argparse
from model import Model
import os
from dataset import create_bin_dataloader
from test import test

def train(positive_path, negative_path, batch_size, epochs, learning_rate, runs_path):
    # Model
    model = Model()
    
    # Train Loader
    train_dataloader = create_bin_dataloader(positive_path, negative_path, batch_size)

    # Training 
    for epoch in range(epochs):
        print(f"epoch {epoch} ==================")
        for i, (imgs, targets) in enumerate(train_dataloader): #=================== batch
            # print("new batch ==================")

            # Forward
            preds = []
            batch_loss = 0
            for img, target in zip(imgs, targets):
                pred = model.forward(img)  # forward
                loss = model.compute_loss(pred, target) # loss scaled by batch_size
                preds += [pred]
                batch_loss += loss
                # print(f"prediction {pred} target {target}")
            print(f"training: batch {i}/{len(train_dataloader)-1} loss {batch_loss/batch_size}")
            
            # Backward
            dW = 0
            dB = 0
            for img, pred, target in zip(imgs, preds, targets):
                # print("========================")
                dw, db = model.find_gradient(img, pred, target)
                dW += dw
                dB += db
            dW /= batch_size
            dB /= batch_size    

            # Opimization
            model.step(learning_rate, dW, dB)

    # save_model
    run_name = time.perf_counter_ns()
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
    parser.add_argument("-r", "--learning_rate", type=float, default=0.1, help="")
    parser.add_argument("--runs", type=str, default="../../data/runs", help="")
    opt = parser.parse_args()
    

    train(opt.positive_path, opt.negative_path, opt.batch_size, opt.epochs, opt.learning_rate, opt.runs)
    