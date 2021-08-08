import argparse
import time
from utils.reference.corner_finder import CornerFinder
from utils.reference.ReferenceSheet import ReferenceSheet
from utils.reference.RotationTranslation import calculateRotationTranslation
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--detect_corners", default=True, type=bool, help="If True will detect corners, else will use already detected from default output")
    parser.add_argument("-b", "--boegen_path", default="../data/boegen", type=str, help="Path to evaluations folder")
    parser.add_argument("-m", "--masks_path", default="../data/masks", type=str, help="Path to masks folder")
    parser.add_argument("-r", "--roi", type=str, default="../data/roi.json", help="Path to file containing roi")
    parser.add_argument("-oc", "--output_corners", type=str, default="../data/corners.json", help="Output json with detected corners for each boegen")
    opt = parser.parse_args()

    if opt.default_corners:
        f = open(opt.roi)
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
            corners = c_finder.find_corners(opt.boegen_path, opt.masks_path, rois)

            json_corners = json.dumps(corners)
            f = open(opt.output_corners, "w")
            f.write(json_corners)
            f.close()

            finish_time = time.perf_counter()
            print(f"Corners detection is finished in {finish_time - start_time} sec for {len(corners)} Boegen")

            for boegen in corners:
                pass
        except Exception as e:
            print(e)

    else:
        pass             


