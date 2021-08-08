import argparse
import cv2
import time
import numpy as np
import math
from multiprocessing import Pool
import os
import json


class CornerFinder:
    
    def count_sum(self, sub_img, corner, pos):
        '''
            Count intersection sum of sub_img with corner
            
            Args: 
                sub_img: part of boegen img 
                corner: corner img
                pos: identifier of sub_img
            Returns:
                c_sum: counted sum
                pos: identifier of sub_img
        '''
        corner_w = corner.shape[1]
        corner_h = corner.shape[0]
        csum = 0
        csum = np.sum(np.bitwise_xor(sub_img, corner))
        n = corner_h * corner_w
        csum /= n

        return (csum, pos)  

    def __find_ul_offset(self, ul):
        '''
            Find ul point offset on img
            
            Args: 
                ul: img with ul corner 
            Returns:
                corner
        '''
        o_y = -1
        o_x = -1

        for y in range(ul.shape[0]):
            if ul[y, ul.shape[1] - 1] == 0:
                o_y = y
                break

        for x in range(ul.shape[1]):
            if ul[ul.shape[0] - 1, x] == 0:
                o_x = x
                break

        return (o_x, o_y) 
            
    def __find_ur_offset(self, ur):
        '''
            Find ur point offset on img
            
            Args: 
                ur: img with ur corner 
            Returns:
                corner
        '''
        o_y = -1
        o_x = -1

        for y in range(ur.shape[0]):
            if ur[y, 0] == 0:
                o_y = y
                break

        for x in range(ur.shape[1]):
            if ur[ur.shape[0] - 1, ur.shape[1] - x - 1] == 0:
                o_x = ur.shape[1] - x - 1
                break

        return (o_x, o_y)

    def __find_ll_offset(self, ll):
        '''
            Find ll point offset on img
            
            Args: 
                ll: img with ll corner 
            Returns:
                corner
        '''
        o_y = -1
        o_x = -1

        for y in range(ll.shape[0]):
            if ll[ll.shape[0] - y - 1, ll.shape[1] - 1] == 0:
                o_y = ll.shape[0] - y - 1
                break

        for x in range(ll.shape[1]):
            if ll[0, x] == 0:
                o_x = x
                break

        return (o_x, o_y)

    def __find_lr_offset(self, lr):
        '''
            Find lr point offset on img
            
            Args: 
                lr: img with lr corner 
            Returns:
                corner
        '''
        o_y = -1
        o_x = -1

        for y in range(lr.shape[0]):
            if lr[lr.shape[0] - y - 1, 0] == 0:
                o_y = lr.shape[0] - y - 1
                break

        for x in range(lr.shape[1]):
            if lr[0, lr.shape[1] - x - 1] == 0:
                o_x = lr.shape[1] - x - 1
                break

        return (o_x, o_y)

    def __img_iter(self, img, corner, roi):
        '''
            Generate iterator over subimages in roi, using corner shape
            
            Args: 
                img: boegen img 
                corner: corner img
                roi: (x, y, w, h)
            Returns:
                subimage: nex sub image
                corner: corner img
                pos: identifier of sub_img
        '''
        img_w = img.shape[1]
        img_h = img.shape[0]
        
        corner_w = corner.shape[1]
        corner_h = corner.shape[0]

        roi_offset_x = (int)(roi[0] * img_w)
        roi_offset_y = (int)(roi[1] * img_h)
        roi_width = (int)(roi[2] * img_w)
        roi_height = (int)(roi[3] * img_h)

        for ih in range(roi_offset_y, roi_offset_y + roi_height - corner_h + 1):
            for iw in range(roi_offset_x, roi_offset_x + roi_width - corner_w + 1):
                yield img[ih:ih + corner_h, iw:iw + corner_w], corner, (iw, ih)

    def __find_corner(self, img, corner, roi):
        '''
            Find cornerss described with masks on boegen using rois
            
            Args: 
                img: boegen
                corner: img of corner to detect on boegen 
                roi: (x, y, w, h)
            Returns:
                corner_pos: (x, y)
        '''
        smallest_sum = math.inf
        corner_pos = (-1,-1)

        with Pool() as pool:
            sums = list(pool.starmap(self.count_sum, self.__img_iter(img, corner, roi)))

        for csum, pos in sums:
            if csum < smallest_sum:
                smallest_sum = csum
                corner_pos = pos        
        return corner_pos

    def find_corners(self, boegen_path, masks_path, rois):
        '''
            Find corners described with masks on boegen using rois
            
            Args: 
                boegen_path: path to dir with boegens
                masks_path: path to dir with masks, that describe corners
                rois: rois in shape (x, y, w, h)
            Returns:
                corners: detected corners of shape path_boegen:[ul, ur, ll, lr]
        '''
        if not os.path.exists(boegen_path):
            raise Exception(f"Boegen folder {boegen_path} doesn't exist")

        boegen = []

        for f in os.listdir(boegen_path):
            if os.path.isdir(f):
                continue
            boegen += [os.path.join(boegen_path, f)]

        masks = [
            os.path.join(masks_path, "ul.png"),
            os.path.join(masks_path, "ur.png"),
            os.path.join(masks_path, "ll.png"),
            os.path.join(masks_path, "lr.png")
            ]

        for mask in masks:
            if not os.path.exists(mask):
                raise Exception(f"File {mask} doesn't exist")

        ul = cv2.imread(masks[0], cv2.IMREAD_GRAYSCALE)
        ur = cv2.imread(masks[1], cv2.IMREAD_GRAYSCALE)
        ll = cv2.imread(masks[2], cv2.IMREAD_GRAYSCALE)
        lr = cv2.imread(masks[3], cv2.IMREAD_GRAYSCALE)

        ul_o = self.__find_ul_offset(ul)
        ur_o = self.__find_ur_offset(ur)
        ll_o = self.__find_ll_offset(ll)
        lr_o = self.__find_lr_offset(lr)

        corners = {}

        i = 0
        for path_evaluation in boegen:
            evaluation = cv2.imread(path_evaluation, cv2.IMREAD_GRAYSCALE)

            ul_pos = self.__find_corner(evaluation, ul, rois[0])
            ur_pos = self.__find_corner(evaluation, ur, rois[1])
            ll_pos = self.__find_corner(evaluation, ll, rois[2])
            lr_pos = self.__find_corner(evaluation, lr, rois[3])

            ul_pos = (ul_pos[0] + ul_o[0], ul_pos[1] + ul_o[1])
            ur_pos = (ur_pos[0] + ur_o[0], ur_pos[1] + ur_o[1])
            ll_pos = (ll_pos[0] + ll_o[0], ll_pos[1] + ll_o[1])
            lr_pos = (lr_pos[0] + lr_o[0], lr_pos[1] + lr_o[1])

            corners[path_evaluation] = (ul_pos, ur_pos, ll_pos, lr_pos)
            i += 1
            # print(f"[{i} / {len(boegen)}]: Corners detected on {path_evaluation}. Corners are {(ul_pos, ur_pos, ll_pos, lr_pos)}")
            print(f"[{i} / {len(boegen)}]: Corners detected on {path_evaluation}")
        return corners

    def draw_corners_n_rois(self, corners, vis_path, rois):
        '''
            Debug function. Saves images with marked rois and detected corners
            
            Args: 
                corners: detected corners
                vis_path: path where debug images will be saved
                rois: rois in shape (x, y, w, h)
            Returns:
                c_sum: counted sum
                pos: identifier of sub_img
        '''
        if os.path.exists(vis_path):
            raise Exception(f"Debug path invalid. Dir {vis_path} already exists")
        else:
            os.mkdir(vis_path)
            

        for i in corners.items():
            f = i[0]
            cs = i[1]

            evaluation = cv2.imread(f)
            if evaluation is None:
                print(f"ERROR: wrong debug corners path: {f}")
                return 

            for corner in cs:
                evaluation = cv2.circle(evaluation, corner, radius=15, color=(0, 0, 255), thickness=3)

            img_w = evaluation.shape[1]
            img_h = evaluation.shape[0]
            
            for roi in rois:
                roi_offset_x = (int)(roi[0] * img_w)
                roi_offset_y = (int)(roi[1] * img_h)
                roi_width = (int)(roi[2] * img_w)   
                roi_height = (int)(roi[3] * img_h)  

                evaluation = cv2.rectangle(evaluation, (roi_offset_x, roi_offset_y), (roi_offset_x + roi_width, roi_offset_y + roi_height), color=(255, 0, 0), thickness=3)

            cv2.imwrite(os.path.join(vis_path, os.path.basename(f)), evaluation)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--boegen_path", default="data/boegen", type=str, help="Path to evaluations folder")
    parser.add_argument("-m", "--masks_path", default="data/masks", type=str, help="Path to masks folder")
    parser.add_argument("-v", "--vis_path", type=str, help="Debug corners detection. Path to folder")
    parser.add_argument("-r", "--roi", type=str, default="data/roi.json", help="Path to file containing roi")
    parser.add_argument("-o", "--output", type=str, default="data/corners.json", help="Output json with detected corners for each boegen", required=True)
    opt = parser.parse_args()

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
        f = open(opt.output, "w")
        f.write(json_corners)
        f.close()

        finish_time = time.perf_counter()
        print(f"Corners detection is finished in {finish_time - start_time} sec for {len(corners)} Boegen")

        if opt.vis_path:
            c_finder.draw_corners_n_rois(corners, opt.vis_path, rois)
    except Exception as e:
        print(e)    



