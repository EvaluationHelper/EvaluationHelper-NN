import argparse
import time
from .reference.corner_finder import CornerFinder
from .reference.ReferenceSheet import ReferenceSheet
import json


def create_reference(_update_corners, _sheets, _masks, _roi, _corners, _transformations, _reference_sheet):
    print("Create Reference ...")
    if _update_corners:
        print("Update corners detection")
        f = open(_roi)
        roi = json.load(f)
        f.close()

        # lux, luy, w, h 
        ul_roi = roi["ul"]
        ur_roi = roi["ur"]
        
        ll_roi = roi["ll"]
        lr_roi = roi["lr"]

        rois = (ul_roi, ur_roi, ll_roi, lr_roi)

        try:
            print("Starting corners detection...")
            start_time = time.perf_counter()
            c_finder = CornerFinder()
            corners = c_finder.find_corners(_sheets, _masks, rois)

            json_corners = json.dumps(corners)
            f = open(_corners, "w")
            f.write(json_corners)
            f.close()

            finish_time = time.perf_counter()
            print(f"Corners detection is finished in {finish_time - start_time} sec for {len(corners)} Sheets")

            sheets = dict()
            reference_corners = corners[_reference_sheet]
            reference_sheet = ReferenceSheet(_reference_sheet, reference_corners[0], reference_corners[1], reference_corners[2], reference_corners[3], [])
            
            for sheet in corners.items():
                cs = sheet[1]
                name = sheet[0]
                s = ReferenceSheet(name, cs[0], cs[1], cs[2], cs[3], [])
                rot_matrix, translation, rot_angle_deg = reference_sheet.calculateRotationTranslation(s)
                sheets[name] = {"rot_matrix" : rot_matrix.tolist(), "translation" : translation.tolist()}

            f = open(_transformations, "w")
            f.write(json.dumps(sheets))
            f.close()
            print(f"Transformations saved to {_transformations}")
        except Exception as e:
            print(f"exception thrown: {e}")

    else:
        print("Count transformation only, use old corners detection")
        f = open(_corners, "r")
        corners = json.load(f)
        f.close()

        sheets = dict()
        reference_corners = corners[_reference_sheet]
        reference_sheet = ReferenceSheet(_reference_sheet, reference_corners[0], reference_corners[1], reference_corners[2], reference_corners[3], [])
        for sheet in corners.items():
            cs = sheet[1]
            name = sheet[0]
            s = ReferenceSheet(name, cs[0], cs[1], cs[2], cs[3], [])
            rot_matrix, translation, rot_angle_deg = reference_sheet.calculateRotationTranslation(s)
            sheets[name] = {"rot_matrix": rot_matrix.tolist(), "translation" : translation.tolist()}

        f = open(_transformations, "w")
        f.write(json.dumps(sheets))
        f.close()
        print(f"Transformations saved to {_transformations}")
    print("Create Reference ... OK")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update_corners", action='store_true', help="If used will detect corners, else will use already detected from default output")
    parser.add_argument("-b", "--boegen", type=str, help="Path to evaluations folder")
    parser.add_argument("-m", "--masks", default="data/masks", type=str, help="Path to masks folder")
    parser.add_argument("-r", "--roi", type=str, default="data/roi.json", help="Path to file containing roi")
    parser.add_argument("-oc", "--corners", type=str, default="data/corners.json", help="Output json with detected corners for each boegen")
    parser.add_argument("-ot", "--transformations", type=str, default="data/transformations.json", help="Output json with rotation and translation for each boegen")
    parser.add_argument("-a", "--annotated_boegen", type=str, default="Bogen1.jpg", help="Path to annotated bogen, that will be used as reference")
    opt = parser.parse_args()

    create_reference(opt.update_corners, opt.boegen, opt.masks, opt.roi, opt.corners, opt.transformations, opt.annotated_boegen)

    


