import numpy as np
import math


def calculateRotationTranslation(reference_sheet_1_lst, reference_sheet_2_lst):
    """
        returns [rotation matrix, translation vector, rotation angle (degree)]
        rot_matrix * reference_sheet_1 + translation = reference_sheet2
    """
    reference_sheet_1_arr = np.array(reference_sheet_1_lst)
    reference_sheet_2_arr = np.array(reference_sheet_2_lst)
    rs1_centroid = calculateCentroid(reference_sheet_1_arr)
    rs2_centroid = calculateCentroid(reference_sheet_2_arr)
    rot_matrix = calculateRotationMatrix(reference_sheet_2_arr, rs2_centroid, reference_sheet_1_arr, rs1_centroid)
    translation = calculateTranslation(rot_matrix, rs2_centroid, rs1_centroid)
    rot_angle_deg = math.degrees(calculateRotationAngle(rot_matrix))
    return [rot_matrix, translation, rot_angle_deg]


def calculateCentroid(points):
    return (np.sum(points, axis=0) / points.shape[0]).transpose()


# http://nghiaho.com/?page_id=671
def calculateRotationMatrix(a, centroid_a, b, centroid_b):
    a_centroid = np.c_[[np.subtract(a_column, centroid_a) for a_column in a]]
    b_centroid = np.c_[[np.subtract(b_column, centroid_b) for b_column in b]]
    h = np.matmul(a_centroid.transpose(), b_centroid)
    u, s, v = np.linalg.svd(h, full_matrices=True)
    return np.matmul(v, np.transpose(u))


def calculateRotationAngle(rotation_matrix):
    # may want to throw exceptions, beware of rounding off errors
    return math.acos(rotation_matrix[0, 0])


def calculateTranslation(rotation_matrix, centroid_a, centroid_b):
    return centroid_b - np.matmul(rotation_matrix, centroid_a)


def calculateRotatedTranslatedFromPoint(point, rotation_matrix, translation):
    return np.matmul(rotation_matrix, point) + translation
