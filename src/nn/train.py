import numpy as np
import argparse
from model import Model
from dataset import DataLoader, DataSet, create_dataloader
from loss import ComputeLoss

def train():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epochs", type=int, default=30, help="Num training epochs")
    opt = parser.parse_args()
    
    # Model
    model = Model()
    
    # Train Loader
    dataset, dataloader = create_dataloader()

    # Loss 
    compute_loss = ComputeLoss(model)

    # Training 
    for epoch in range(opt.epochs):
        model.train()

        pbar = enumerate(dataloader)
        for i, (imgs, targets) in pbar: #=================== batch

            # Forward
            pred = model.forward(imgs)  # forward
            loss = compute_loss(pred, targets)  # loss scaled by batch_size

            # Backward
            model.backward(loss)

            # Optimize 
            model.update()
