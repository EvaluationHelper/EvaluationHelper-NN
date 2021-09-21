from utils.create_reference import create_reference
from utils.reference.corner_cutter import cut_boxes
from nn.model import Model
from nn.detect import create_annotation, save_annotation
from utils.create_statistics import create_print_statistics
import os

cwd = os.getcwd()
root_path, tail = os.path.split(cwd)


def get_absolute_paths(relative_paths=["data/roi.json",
                                       "data/masks",
                                       "data/transformations.json",
                                       "data/corners.json",
                                       "data/boxes",
                                       "data"]):
    abs_paths = []
    for path in relative_paths:
        abs_paths.append(os.path.normpath(os.path.join(root_path, path)))
    return abs_paths


if __name__ == '__main__':

    # get path to sheets from user
    usr_boegen_path = input("Please enter path to scanned sheets to be evaluated:\n")

    # construct absolute paths to be used as args
    paths = get_absolute_paths()
    reference_sheet_name = "Bogen1.jpg"

    # detect corners and determine transformation to reference sheet
    # create_reference(False, usr_boegen_path, paths[1], paths[0], paths[3], paths[2], reference_sheet_name)

    # cut out every box
    cut_boxes(paths[3],
              sheet_path=usr_boegen_path,
              box_path=os.path.normpath(os.path.join(root_path, "data/boxes/")),
              reference_json_path=os.path.normpath(os.path.join(root_path, "data/Bogen1ReferencePoints.json")))

    # load nn model
    model = Model(paths[5])

    # make predictions w/ model and save as json
    annotation = create_annotation(model, paths[4])
    save_annotation(annotation, paths[5])

    # print out statistics about evaluation
    create_print_statistics(root_path, "data/annotation.json")
