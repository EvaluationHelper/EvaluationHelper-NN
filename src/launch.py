from create_reference import create_reference
from utils.reference.corner_cutter import cut_boxes
from nn.model import Model
from nn.detect import create_annotation, save_annotaion
from utils.create_statistics import create_print_statistics
import os

cwd = os.getcwd()

def get_absolute_paths(relative_paths = ['data/roi.json', "data/masks", "data/transformations.json", "data/corners.json"]):
    cwd = os.getcwd()
    abs_paths = []
    for path in relative_paths:
        abs_paths.append(os.path.join(cwd, path))
    return abs_paths

if __name__ == '__main__':

    #get path to sheets from user
    usr_boegen_path = input("Please enter path to scanned sheets to be evaluated:\n")

    #construct absolute paths to be used as args
    paths = get_absolute_paths()

    #detect corners and determine transformation to reference sheet
    create_reference(False, paths[0], usr_boegen_path, paths[1], paths[2], paths[3])

    #cut out every box
    cut_boxes(paths[3], sheet_path=usr_boegen_path)

    #load nn model
    model = Model(os.path.join(cwd, 'data/'))

    # make predictions w/ model and save as json
    annotation = create_annotation(model)
    save_annotaion(annotation)

    # print out statistics about evaluation
    create_print_statistics(cwd)