import os
import argparse

def split_train_test(path_pos, path_neg, path_train, path_test, coef):
    if not os.path.exists(path_pos) or not os.path.exists(path_neg):
        raise Exception(f"wrong dataset path") 
    if os.path.exists(path_train):
        os.rmdir(path_train)
    if os.path.exists(path_test):
        os.rmdir(path_test)
    
    pos_dir = os.path.basename(path_pos)
    neg_dir = os.path.basename(path_neg)
    os.mkdir(path_train)
    os.mkdir(path_test)    
    os.mkdir(os.path.join(path_train, pos_dir))
    os.mkdir(os.path.join(path_train, neg_dir))
    os.mkdir(os.path.join(path_test, pos_dir))
    os.mkdir(os.path.join(path_test, neg_dir))
    
    num_pos = len(os.listdir(path_pos))
    size_train_pos = int(num_pos * coef)

    num_neg = len(os.listdir(path_neg))
    size_train_neg = int(num_neg * coef)

    
    train_pos = os.listdir(path_pos)[:size_train_pos]
    test_pos = os.listdir(path_pos)[size_train_pos:]
    train_neg = os.listdir(path_neg)[:size_train_neg]
    test_neg = os.listdir(path_neg)[size_train_neg:]

    print(f"Positive total: {num_pos}\nNegative total: {num_neg}\nTrain positive: {len(train_pos)}\nTrain negative: {len(train_neg)}\
        \nTest positive: {len(test_pos)}\nTest negative: {len(test_neg)}")

    for f in train_pos:
        os.rename(os.path.join(path_pos, f), os.path.join(path_train, pos_dir, f))

    for f in train_neg:
        os.rename(os.path.join(path_neg, f), os.path.join(path_train, neg_dir, f))    

    for f in test_pos:
        os.rename(os.path.join(path_pos, f), os.path.join(path_test, pos_dir, f))

    for f in test_neg:
        os.rename(os.path.join(path_neg, f), os.path.join(path_test, neg_dir, f))        
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path_pos", type=str, default="../../../data/dataset/work_type_crossed", help="Path to evaluations folder")
    parser.add_argument("-n", "--path_neg", type=str, default="../../../data/dataset/work_type_empty", help="Path to masks folder")
    parser.add_argument("-tr", "--path_train", type=str, default="../../../data/dataset/train", help="Debug corners detection. Path to folder")
    parser.add_argument("-te", "--path_test", type=str, default="../../../data/dataset/test", help="Path to file containing roi")
    parser.add_argument("-c", "--coef", type=float, help="Output json with detected corners for each boegen", required=True)
    opt = parser.parse_args()    

    split_train_test(opt.path_pos, opt.path_neg, opt.path_train, opt.path_test, opt.coef)