import json
from src.RotationTranslation import calculateRotationTranslation, calculateRotatedTranslatedFromPoint


class ReferenceSheet:
    def __init__(self, upper_left, upper_right, bottom_left, bottom_right, *questions):
        self._u_r = upper_right
        self._u_l = upper_left
        self._b_r = bottom_right
        self._b_l = bottom_left
        self._questions = questions

    def calculateRotationTranslation(self, target_ref_sheet):
        """
            :type target_ref_sheet: ReferenceSheet
        """
        return calculateRotationTranslation(
            [self._u_l, self._u_r, self._b_r, self._b_l],
            [target_ref_sheet._u_l, target_ref_sheet._u_r, target_ref_sheet._b_r, target_ref_sheet._b_l])

    def calculateRotatedTranslatedFromSheet(self, rotation_matrix, translation):
        return [calculateRotatedTranslatedFromPoint(point) for point in [self._u_l, self._u_r, self._b_r, self._b_l]]


class Question:
    def __init__(self, *boxes):
        self._boxes = boxes
        self._answers = len(self._boxes)


class Box:
    def __init__(self, upper_left, bottom_right):
        self._u_l = upper_left
        self._b_r = bottom_right


if __name__ == "__main__":
    box1 = Box([0, 1], [1, 0])
    box2 = Box([2, 1], [3, 0])
    question1 = Question(box1, box2)
    referenceSheet1 = ReferenceSheet([-4, 3], [3, 3], [-4, -7], [3, -7], question1)

    box1_2 = Box([0, 1], [1, 0])
    box2_2 = Box([2, 1], [3, 0])
    question1_2 = Question(box1_2, box2_2)
    referenceSheet2 = ReferenceSheet([-2, 5], [5, 5], [-2, -5], [5, -5], question1_2)

    print(referenceSheet1.calculateRotation(referenceSheet2)[1])