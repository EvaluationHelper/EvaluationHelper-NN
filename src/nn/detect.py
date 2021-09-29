from PIL import Image
import os
import numpy as np
import json

from nn.model import Model


def create_annotation(model, boxes_path='../../data/boxes/'):
    """
    predicts if boxes are checked with NN model
    creates a dictionary with information about all boxes:
        Keys: path and name to cut-out box (string)
        Values: 1 if checked, 0 if unchecked
    """
    print("Create Annotation ...")
    images = dict()
    annotation  = []

    for f in os.listdir(boxes_path):
        path = os.path.join(boxes_path,f)
        image = np.array(Image.open(path))

        if image is None:
                raise Exception(f"wrong file path for boxes-ticked detection : {path}")
                
        vec_img = np.reshape(image, (image.shape[0] * image.shape[1]))
        vec_img = vec_img.astype('float64')
        vec_img /= 255
        images[path] = np.array([vec_img])

    for path in images:
        box_dict = dict()        
        prediction = model.forward(images[path]) #make prediction with NN
        ticked_state = int(round(prediction[0][1]))
        box_dict[path] = ticked_state
        annotation.append(box_dict)

    print("Create Annotation ... OK")
    return annotation


def save_annotation(annotation, annotation_dir='../../data'):
    """
    Saves dictionary a a json file
    """
    print("Save Annotation ...")
    annotations_path = os.path.join(annotation_dir, "annotation.json")
    f = open(annotations_path,"w")
    f.write(json.dumps(annotation))
    f.close
    print("Save Annotation ... OK")


if __name__ == '__main__':
    '''''
    model.json for the trained model should be places in /data/
    pictures of boxes are saved in /data/boxes/
    annotations.json contains path with name of each box and corresponding boolean (ticked = 1, unticked = 0)
    '''''
    model = Model('../../data/')
    annotation = create_annotation(model)
    save_annotation(annotation)
