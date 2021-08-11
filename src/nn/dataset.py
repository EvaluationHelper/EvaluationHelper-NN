import os
import random
import cv2

class DataLoader():
    def __init__(self, dataset, batch_size):
        self.dataset = dataset
        self.bath_size = batch_size
        self.i = -1
       

    def __len__(self):
        return len(self.dataset) // self.bath_size   

    def __next__(self):
        self.i += 1
        if self.i == len(self):
            raise StopIteration
        batch = []
        for path, label in self.dataset[self.i * self.bath_size : self.i * self.bath_size + self.bath_size]:
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise Exception(f"wrong file path in batch generation(data loader): {path}")
            batch += [(img, label)]    
        return batch

    def __iter__(self):
        return self
    

def create_bin_dataloader(pos_data_path, neg_data_path, batch_size):
    if not os.path.exists(pos_data_path):
        raise Exception(f"wrong pos_data_path data loader: {pos_data_path}")
        
    if not os.path.exists(neg_data_path):
        raise Exception(f"wrong neg_data_path data loader: {neg_data_path}")

    paths_labeld = []
    for f in os.listdir(pos_data_path):
        paths_labeld += [(f, 1)]

    for f in os.listdir(neg_data_path):
        paths_labeld += [(f, 0)]   

    random.shuffle(paths_labeld)
    dataloader = DataLoader(paths_labeld, batch_size)
    return dataloader
