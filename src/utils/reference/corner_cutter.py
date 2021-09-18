import json
import os.path
from utils.reference.ReferenceSheet import *
from PIL import Image


def __read_sheet_json__(path):
    """
        create ReferenceSheet from json containing question and box positions

        Args:
            path: path to the sheet
        Returns:
            object of class src.utils.reference.ReferenceSheet.ReferenceSheet
    """
    file = open(path)
    sheet_json = json.load(file)
    file.close()

    sheet_box_positions = sheet_json.get("boxPositions")
    question_lst = []
    for question_key in sheet_box_positions.keys():
        question_lst.append(
            Question(question_key,
                     *[Box(box_key,
                           sheet_box_positions.get(question_key).get(box_key).get("upperLeft"),
                           sheet_box_positions.get(question_key).get(box_key).get("bottomRight"))
                       for box_key in sheet_box_positions.get(question_key).keys()]))

    return ReferenceSheet(sheet_json.get("name"),
                          sheet_json.get("referencePoints").get("upperLeft"),
                          sheet_json.get("referencePoints").get("upperRight"),
                          sheet_json.get("referencePoints").get("bottomLeft"),
                          sheet_json.get("referencePoints").get("bottomRight"),
                          *question_lst)


def __save_box__(img, box, path_prefix, box_path, ext='.jpg', puffer=20, size=40):
    """
        crops image based on box coordinates, resizes and saves it

        Args:
            img: large image
            box: object of class src.utils.reference.ReferenceSheet.Box
            path_prefix: prefix for savename
            box_path: path to boxes
            ext: extension type
            puffer: crop image with puffer around corners
            size: resize size
    """
    box_u_l, box_b_r = box.get_points()
    img_crop = img.crop((box_u_l[0] - puffer, box_u_l[1] - puffer,
                         box_b_r[0] + puffer, box_b_r[1] + puffer))
    img_res = img_crop.resize((size, size))

    path = os.path.join(box_path, path_prefix + "_" + box.get_name() + ext)
    box.set_path(path)
    img_res.save(path)


def cut_boxes(corners_path, sheet_path, box_path, reference_json_path):
    """
        rotates, translates, cuts and saves boxes based on corner data and reference sheet data

        Args:
            corners_path: path to json containing all sheets with their corners
            sheet_path: path to sheet folder
            box_path: path to box folder
            reference_json_path: path to reference json
    """
    print("Cut Boxes ...")
    reference_sheet = __read_sheet_json__(reference_json_path)
    file = open(corners_path)
    corners = json.load(file)
    file.close()

    sheet_lst = [ReferenceSheet(key,
                                corners.get(key)[0], corners.get(key)[1],
                                corners.get(key)[2], corners.get(key)[3])
                 for key in corners.keys()]

    for sheet in sheet_lst:
        # rotate and translate back to coordinates of ref_sheet1
        rot_m, tl, rot_a = sheet.calculateRotationTranslation(sheet_lst[0])
        image = Image.open(os.path.join(sheet_path, sheet.get_name()))
        image_rot_tl = image.transform(image.size, Image.AFFINE,
                                       (rot_m[0][0], rot_m[0][1], tl[0],
                                        rot_m[1][0], rot_m[1][1], tl[1]))

        for question in reference_sheet.get_questions():
            for box in question.get_boxes():
                __save_box__(image_rot_tl, box,
                             os.path.splitext(sheet.get_name())[0] + "_" + question.get_name(), box_path)
    print("Cut Boxes ... OK")
