import json
import os.path
from src.utils.reference.ReferenceSheet import *
from PIL import Image


def __read_sheet_json__(path):
    file = open(path)
    sheet_json = json.load(file)
    file.close()

    # Todo: not pretty at, all this ugly as hell
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


def __save_box__(img, box, path_suffix):
    puffer = 20
    box_u_l, box_b_r = box.get_points()
    img_crop = img.crop((box_u_l[0] - puffer, box_u_l[1] - puffer,
                         box_b_r[0] + puffer, box_b_r[1] + puffer))
    img_res = img_crop.resize((40, 40))
    img_res.save("../../../data/boxes/" + path_suffix + "_" + box.get_name() + ".jpg")
    print("Saved to ../../../data/boxes/" + path_suffix + "_" + box.get_name() + ".jpg")
    return None


def __cut_box_single__():
    return None


# acting as main right now
def cut_boxes(corners_path):
    reference_sheet = __read_sheet_json__("../../../data/Bogen1ReferencePoints.json")
    file = open(corners_path)
    corners = json.load(file)
    file.close()

    sheet_lst = [ReferenceSheet(key,
                                corners.get(key)[0], corners.get(key)[1],
                                corners.get(key)[2], corners.get(key)[3])
                 for key in corners.keys()]

    # do all the work here
    for sheet in sheet_lst:
        # rotate and translate back to coordinates of ref_sheet1
        rot_m, tl, rot_a = sheet.calculateRotationTranslation(sheet_lst[0])
        """
        print(rot_m)
        print(tl)
        print(rot_a)
        print("------------ RefSheet ----------")
        for a in sheet_lst[0].get_reference_points():
            print(a)
        print("------------ compSheet ----------")
        for a in sheet.get_reference_points():
            print(a)
        print("------------ onlyRot ----------")
        for a in sheet.calculateRotatedTranslatedFromSheet(rot_m, [0, 0]):
            print(a)
        print("------------ transRot ----------")
        for a in sheet.calculateRotatedTranslatedFromSheet(rot_m, tl):
            print(a)
        """
        image = Image.open(r"../../../data/boegen/" + sheet.get_name())
        image_rot_tl = image.transform(image.size, Image.AFFINE,
                                       (rot_m[0][0], rot_m[0][1], tl[0],
                                        rot_m[1][0], rot_m[1][1], tl[1]))

        for question in reference_sheet.get_questions():
            for box in question.get_boxes():
                __save_box__(image_rot_tl, box,
                             os.path.splitext(sheet.get_name())[0] + "_" + question.get_name())
    return None


if __name__ == '__main__':
    cut_boxes("../../../data/corners.json")
