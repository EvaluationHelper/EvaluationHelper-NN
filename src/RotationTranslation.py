import numpy as np
import math


def calculateRotationTranslation(reference_sheet_1_lst, reference_sheet_2_lst):
    """
        returns [rotation matrix, translation vector, rotation angle (radians), rotation angle (degree)]
    """
    reference_sheet_1_arr = np.array(reference_sheet_1_lst)
    reference_sheet_2_arr = np.array(reference_sheet_2_lst)
    rs1_centroid = calculateCentroid(reference_sheet_1_arr)
    rs2_centroid = calculateCentroid(reference_sheet_2_arr)
    rot_matrix = calculateRotationMatrix(reference_sheet_1_arr, rs1_centroid, reference_sheet_2_arr, rs2_centroid)
    translation = calculateTranslation(rot_matrix, rs1_centroid, rs2_centroid)
    rot_angle_rad = calculateRotationAngle(rot_matrix)
    rot_angle_deg = math.degrees(rot_angle_rad)
    return [rot_matrix, translation, rot_angle_rad, rot_angle_deg]


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
    if math.acos(rotation_matrix[0, 0]) != math.asin(rotation_matrix[1, 0]):
        raise Exception('Wrong calculation of Rotation Matrix (theta)')
    return math.acos(rotation_matrix[0, 0])


def calculateTranslation(rotation_matrix, centroid_a, centroid_b):
    return centroid_b - np.matmul(rotation_matrix, centroid_a)


def calculateRotatedTranslatedFromPoint(point, rotation_matrix, translation):
    return np.matmul(rotation_matrix, point) + translation


'''
if __name__ == "__main__":
    c_tmp = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    c2_tmp = [[2, 3], [1, 2], [2, 1], [3, 2]]
    c = np.array(c_tmp)
    c2 = np.array(c2_tmp)

    centroid_c = calculateCentroid(c)
    centroid_c2 = calculateCentroid(c2)
    rot_matrix = calculateRotationMatrix(c, centroid_c, c2, centroid_c2)
    translation = calculateTranslation(rot_matrix, centroid_c, centroid_c2)
    rot_angle_rad = calculateRotationAngle(rot_matrix)
    rot_angle_deg = math.degrees(rot_angle_rad)

    print(rot_matrix)
    print(calculateTranslation(rot_matrix, centroid_c, centroid_c2))
    print(np.matmul(calculateRotationMatrix(c, centroid_c, c2, centroid_c2), c.T))
    print(calculateRotationAngle(rot_matrix), math.degrees(calculateRotationAngle(rot_matrix)))
'''