import time
import argparse
import os
import json

from nn.model import Model
from nn.dataset import create_bin_dataloader
from nn.test import test


def train(positive_path, negative_path, batch_size, epochs, learning_rate, runs_path, test_positive, test_negative):
    """
    Train & test & save the NN
    Args: 
        positive_path : path to train crossed boxes 
        negative_path : path to train not-crossed boxes
        batch_size : training batch size
        epochs : number of training epochs
        learning_rate : training step rate
        runs_path : path to save runs information
        test_positive : path to test crossed boxes
        test_negative : path to test not-crossed boxes
    Returns: 
        ...      
    """
    # run dir
    run_name = time.perf_counter_ns()
    run_dir = os.path.normpath(os.path.join(runs_path, "run_" + str(run_name)))
    os.mkdir(run_dir)

    train_info = dict()
    train_info["num epochs"] = epochs
    train_info["batch size"] = batch_size
    f = open(os.path.normpath(os.path.join(run_dir, "train_info.json"), "w"))
    f.write(json.dumps(train_info))
    f.close()

    # Model
    model = Model()

    # Train Loader
    train_dataloader = create_bin_dataloader(positive_path, negative_path, batch_size)

    # Training 
    for epoch in range(epochs):
        print(f"epoch {epoch} / {epochs}")
        for i, (imgs, targets) in enumerate(train_dataloader): #=================== batch

            # Forward
            preds = []
            batch_loss = 0
            for img, target in zip(imgs, targets):
                pred = model.forward(img)  # forward
                loss = model.compute_loss(pred, target) # loss scaled by batch_size
                preds += [pred]
                batch_loss += loss
                
            # Backward
            dW = 0
            dB = 0
            for img, pred, target in zip(imgs, preds, targets):
        
                dw, db = model.find_gradient(img, pred, target)
                dW += dw
                dB += db
            dW /= batch_size
            dB /= batch_size    

            # Opimization
            model.step(learning_rate, dW, dB)


    # save_model
    model_path = os.path.normpath(os.path.join(run_dir, "model.json"))
    model.save_model(model_path)

    # test 
    test(model, test_positive, test_negative, os.path.normpath(os.path.join(run_dir, "metrics.json")))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epochs", type=int, default=30, help="number of training epochs")
    parser.add_argument("-b", "--batch_size", type=int, default=50, help="training batch size")
    parser.add_argument("-p", "--positive_path", type=str, default="../../data/dataset/train/work_type_crossed", help="path to train crossed boxes")
    parser.add_argument("-n", "--negative_path", type=str, default="../../data/dataset/train/work_type_empty", help="path to train not-crossed boxes")
    parser.add_argument("-r", "--learning_rate", type=float, default=0.1, help="training step rate")
    parser.add_argument("--runs", type=str, default="../../data/runs", help="path to save runs information")
    parser.add_argument("-tp", "--test_positive", default="../../data/dataset/test/work_type_crossed", type=str, help="path to test crossed boxes")
    parser.add_argument("-tn", "--test_negative", default="../../data/dataset/test/work_type_empty", type=str, help="path to test not-crossed boxes")
    
    opt = parser.parse_args()

    train(opt.positive_path, opt.negative_path, opt.batch_size, opt.epochs, opt.learning_rate, opt.runs, opt.test_positive, opt.test_negative)
