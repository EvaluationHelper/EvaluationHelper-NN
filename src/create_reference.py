import argparse
import time
from utils.reference.corner_finder import CornerFinder
from utils.reference.ReferenceSheet import ReferenceSheet
import json

def create_reference(update_corners, roi, boegen_path, masks_path, output_transformation, output_corners):
    if update_corners:
        print("Update corners detection")
        f = open(roi)
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
            corners = c_finder.find_corners(boegen_path, masks_path, rois)

            json_corners = json.dumps(corners)
            f = open(opt.output_corners, "w")
            f.write(json_corners)
            f.close()

            finish_time = time.perf_counter()
            print(f"Corners detection is finished in {finish_time - start_time} sec for {len(corners)} Boegen")

            boegens = dict()
            reference_corners = corners['Bogen1.jpg']
            reference_sheet = ReferenceSheet(reference_corners[0], reference_corners[1], reference_corners[2], reference_corners[3], [])
            for boegen in corners.items():
                cs = boegen[1]
                name = boegen[0]
                s = ReferenceSheet(cs[0], cs[1], cs[2], cs[3], [])
                rot_matrix, translation, rot_angle_deg = reference_sheet.calculateRotationTranslation(s)
                boegens[name] = {"rot_matrix" : rot_matrix.tolist(), "translation" : translation.tolist()}

            f = open(output_transformation, "w")
            f.write(json.dumps(boegens))
            f.close()
            print(f"Transformations saved to {output_transformation}")
        except Exception as e:
            print(e)

    else:
        print("Use old corners detection")
        f = open(output_corners, "r")
        corners = json.load(f)
        f.close()

        boegens = dict()
        reference_corners = corners['Bogen1.jpg']
        reference_sheet = ReferenceSheet(reference_corners[0], reference_corners[1], reference_corners[2], reference_corners[3], [])
        for boegen in corners.items():
            cs = boegen[1]
            name = boegen[0]
            s = ReferenceSheet(cs[0], cs[1], cs[2], cs[3], [])
            rot_matrix, translation, rot_angle_deg = reference_sheet.calculateRotationTranslation(s)
            boegens[name] = {"rot_matrix" : rot_matrix.tolist(), "translation" : translation.tolist()}

        f = open(opt.output_transformation, "w")
        f.write(json.dumps(boegens))
        f.close()
        print(f"Transformations saved to {output_transformation}")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update_corners", action='store_true', help="If used will detect corners, else will use already detected from default output")
    parser.add_argument("-b", "--boegen_path", default="../data/boegen", type=str, help="Path to evaluations folder")
    parser.add_argument("-m", "--masks_path", default="../data/masks", type=str, help="Path to masks folder")
    parser.add_argument("-r", "--roi", type=str, default="../data/roi.json", help="Path to file containing roi")
    parser.add_argument("-oc", "--output_corners", type=str, default="../data/corners.json", help="Output json with detected corners for each boegen")
    parser.add_argument("-ot", "--output_transformation", type=str, default="../data/transformations.json", help="Output json with rotation and translation for each boegen")
    #parser.add_argument("-a", "--annotated_bogen", type=str, default="../data/boegen/Bogen1.jpg", help="Path to annotated bogen, that will be used as reference")
    #annotated_bogen is expected to be the name of annotated sheet, not path -> arg needed?
    opt = parser.parse_args()

    create_reference(opt.update_corners, opt.roi, opt.boegen_path, opt.masks_path, opt.output_transformation, opt.corners)
    


