import numpy as np
import argparse
from model import Model
from dataset import DataLoader, DataSet, create_dataloader
from loss import ComputeLoss

def train(train_path, batch_size, epochs, learning_rate):
    # Model
    model = Model()
    
    # Train Loader
    dataset, dataloader = create_dataloader(opt.train_path, opt.batch_size)

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
            model.step()
            model.update()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epochs", type=int, default=30, help="Num training epochs")
    parser.add_argument("-b", "--batch_size", type=int, default=50, help="Num training epochs")
    parser.add_argument("-t", "--train_path", type=str, default="../../data/boxes", help="Num training epochs")
    parser.add_argument("-r", "--learning_rate", type=str, default="../../data/boxes", help="Num training epochs")
    opt = parser.parse_args()
    

    train(opt.train_path, opt.batch_size, opt.epochs, opt.learning_rate)
    