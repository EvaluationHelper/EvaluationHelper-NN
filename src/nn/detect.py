from model import Model
import cv2
import os
import numpy as np
import json

def get_annotation(boxes_path='../../data/boxes/'):

    images = dict()
    annotation  = []

    for f in os.listdir(boxes_path):
        path = os.path.join(boxes_path,f)
        image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

        if image is None:
                raise Exception(f"wrong file path for boxes-ticked detection : {path}")
                
        vec_img = np.reshape(image, (image.shape[0] * image.shape[1]))
        vec_img = vec_img.astype('float64')
        vec_img /= 255
        images[path] = np.array([vec_img])

    for path in images:
        box_dict = dict()        
        prediction = model.forward(images[path])
        ticked_state = int(round(prediction[0][1]))
        box_dict[path] = ticked_state
        annotation.append(box_dict)

    return [annotation] 


def save_annotaion(annotation, annotation_dir='../../data'):
    annotations_path = os.path.join(annotation_dir, "annotation.json")
    f = open(annotations_path,"w")
    f.write(json.dumps(annotation))
    f.close



if __name__ == '__main__':
    
    '''''
    model.json for the trained model should be places in /data/
    pictures of boxes are saved in /data/boxes/
    annotations.json contains path with name of each box and corresponding boolean (ticked = 1, unticked = 0)
    '''''

    model = Model('../../data/')
    annotation = get_annotation()
    save_annotaion(annotation)
