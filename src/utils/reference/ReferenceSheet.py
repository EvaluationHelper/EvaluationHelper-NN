from src.utils.reference.RotationTranslation import calculateRotationTranslation, calculateRotatedTranslatedFromPoint


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
    def __init__(self, name, upper_left, bottom_right, path=None, is_checked=None):
        self._name = name
        self._u_l = upper_left
        self._b_r = bottom_right
        self._path = path
        self._is_checked = is_checked

    def get_name(self):
        return self._name

    def get_points(self):
        return self._u_l, self._b_r

    def get_is_checked(self):
        return self._is_checked

    def set_is_checked(self, new_is_checked):
        self._is_checked = new_is_checked

    def set_path(self, new_path):
        self._path = new_path

    def get_path(self):
        return self._path

    def asdict(self):
        return {'upperLeft': self._u_l,
                'bottomRight': self._b_r,
                'path': self._path,
                'is_checked': self._is_checked}




