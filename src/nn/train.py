import numpy as np
import argparse
from model import Model
from dataset import create_bin_dataloader
from loss import ComputeLoss

def train(positive_path, negative_path, batch_size, epochs, learning_rate):
    # Model
    model = Model()
    
    # Train Loader
    dataloader = create_bin_dataloader(positive_path, negative_path, batch_size)

    # Loss 
    compute_loss = ComputeLoss(model)

    # Training 
    for epoch in range(epochs):

        for i, (imgs, targets) in enumerate(dataloader): #=================== batch

            # Forward
            pred = model.forward(imgs)  # forward
            loss = compute_loss(pred, targets)  # loss scaled by batch_size

            # Backward
            model.backward(loss)

            # Opimization
            model.step(learning_rate)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epochs", type=int, default=30, help="")
    parser.add_argument("-b", "--batch_size", type=int, default=50, help="")
    parser.add_argument("-p", "--positive_path", type=str, default="", help="")
    parser.add_argument("-n", "--negative_path", type=str, default="", help="")
    parser.add_argument("-r", "--learning_rate", type=str, default="", help="")
    parser.add_argument("-a", "--annotaion_path", type=str, default="", help="")
    opt = parser.parse_args()
    

    train(opt.positive_path, opt.negative_path, opt.batch_size, opt.epochs, opt.learning_rate)
    