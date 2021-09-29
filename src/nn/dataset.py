import os
import random
from PIL import Image
import numpy as np

class DataLoader():
    def __init__(self, dataset, batch_size):
        self.dataset = dataset
        self.bath_size = batch_size
        self.i = -1
       

    def __len__(self):
        return len(self.dataset) // self.bath_size   

    def __next__(self):
        self.i += 1
        if self.i >= len(self):
            self.i = -1
            raise StopIteration
        batch = [[], []]
        for path, label in self.dataset[self.i * self.bath_size : self.i * self.bath_size + self.bath_size]:
            img = np.array(Image.open(path))
            if img is None:
                raise Exception(f"wrong file path in batch generation(data loader): {path}")
            
            vec_img = np.resize(img, (img.shape[0] * img.shape[1]))
            vec_img = vec_img.astype('float64')
            vec_img /= 255.

            batch[0] += [np.array([vec_img])]
            batch[1] += [label]   
        return batch

    def __iter__(self):
        return self
    

def create_bin_dataloader(pos_data_path, neg_data_path, batch_size):
    '''
    Create dataloader for crossed/not-crossed dataset, to iterate over batches 
    Args: 
        pos_data_path : path to crossed boxes
        neg_data_path : path to not-crossed boxes
    Returns: 
        dataloader : iterable      
    '''
    if not os.path.exists(pos_data_path):
        raise Exception(f"wrong pos_data_path data loader: {pos_data_path}")
        
    if not os.path.exists(neg_data_path):
        raise Exception(f"wrong neg_data_path data loader: {neg_data_path}")

    paths_labeld = []
    for f in os.listdir(pos_data_path):
        paths_labeld += [(os.path.normpath(os.path.join(pos_data_path, f)), np.array([0, 1]))]

    for f in os.listdir(neg_data_path):
        paths_labeld += [(os.path.normpath(os.path.join(neg_data_path, f)), np.array([1, 0]))]

    random.shuffle(paths_labeld)
    dataloader = DataLoader(paths_labeld, batch_size)
    return dataloader
