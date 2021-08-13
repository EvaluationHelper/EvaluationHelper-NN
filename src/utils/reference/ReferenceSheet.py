from src.utils.reference.RotationTranslation import calculateRotationTranslation, calculateRotatedTranslatedFromPoint
from PIL import Image
import json


class ReferenceSheet:
    def __init__(self, name, upper_left, upper_right, bottom_left, bottom_right, *questions):
        self._name = name
        self._u_l = upper_left
        self._u_r = upper_right
        self._b_l = bottom_left
        self._b_r = bottom_right
        self._questions = questions

    def calculateRotationTranslation(self, target_ref_sheet):
        """
            :type target_ref_sheet: ReferenceSheet
        """
        return calculateRotationTranslation(
            [self._u_l, self._u_r, self._b_l, self._b_r],
            [target_ref_sheet._u_l, target_ref_sheet._u_r, target_ref_sheet._b_l, target_ref_sheet._b_r])

    def calculateRotatedTranslatedFromSheet(self, rotation_matrix, translation):
        return [calculateRotatedTranslatedFromPoint(point, rotation_matrix, translation)
                for point in [self._u_l, self._u_r, self._b_l, self._b_r]]

    def get_name(self):
        return self._name

    def get_questions(self):
        return self._questions

    def get_reference_points(self):
        return self._u_l, self._u_r, self._b_l, self._b_r

    def asdict(self):
        return {'name': self._name,
                'referencePoints': {
                    'upperLeft': self._u_l,
                    'upperRight': self._u_r,
                    'bottomLeft': self._b_l,
                    'bottomRight': self._b_r,
                    },
                'boxPositions': [question.asdict() for question in self._questions]}


class Question:
    def __init__(self, name, *boxes):
        self._name = name
        self._boxes = boxes
        self._answers = len(self._boxes)

    def get_name(self):
        return self._name

    def get_boxes(self):
        return self._boxes

    def asdict(self):
        return {self._name: {'boxes': [box.asdict() for box in self._boxes]}}


class Box:
    def __init__(self, name, upper_left, bottom_right):
        self._name = name
        self._u_l = upper_left
        self._b_r = bottom_right

    def get_name(self):
        return self._name

    def get_points(self):
        return self._u_l, self._b_r

    def asdict(self):
        return {'upperLeft': self._u_l,
                'bottomRight': self._b_r}


if __name__ == "__main__":

    # Data from coner_finder.py
    box1 = Box([0, 1], [1, 0])
    box2 = Box([2, 1], [3, 0])
    box3 = Box([4, 1], [5, 0])
    lst = [box1, box2, box3]
    question1 = Question('question1', box1, box2, box3)
    question2 = Question('question2', box3, box2, box1)
    referenceSheet1 = ReferenceSheet('Bogen1', [1134, 388], [2354, 387], [1133, 2785], [2356, 2783], question1, question2)
    referenceSheet28 = ReferenceSheet('Bogen28', [1153, 390], [2374, 389], [1151, 2778], [2372, 2781])

    # calculate rotation and translation for which ref1 must be rotated to fit ref28
    # may need to adjust if the other way around is wanted
    rot_matrix, translation, rot_angle_deg = referenceSheet1.calculateRotationTranslation(referenceSheet28)
    print(rot_matrix)
    print(translation)
    print(rot_angle_deg)
    print(json.dumps(referenceSheet1.asdict()))
    print(json.dumps(referenceSheet28.asdict()))

    image_ref_1 = Image.open(r"../../../data/boegen/Bogen1.jpg")
    image_ref_28 = Image.open(r"../../../data/boegen/Bogen28.jpg")
    image_ref_1_rot = image_ref_1.rotate(referenceSheet1.calculateRotationTranslation(referenceSheet28)[2])
    image_ref_1_rot = image_ref_1_rot.transform(image_ref_1_rot.size, Image.AFFINE,
                                                (1, 0, translation[0],
                                                 0, 1, translation[1]))

    #image_ref_1.show()
    #image_ref_1_rot.show()
    #image_ref_28.show()



