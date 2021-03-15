"""Robotic Simulation Software Sensor model for Localization
Authors:
Sergi Nogues Farres
"""
import numpy as np


def feature(pose, feature_coord):
    """
    :param feature_coord: feature [x, y]
    :param pose: robot pose [x y, theta]
    :return: [distance, bearing, signature, x, y]
    """
    # ToDo: add noise and signature
    distance = np.sqrt((feature_coord[0] - pose[0]) ** 2 + (feature_coord[1] - pose[1]) ** 2)  # + np.random.random()
    bearing = np.arctan2(feature_coord[1] - pose[1], feature_coord[0] - pose[0]) - pose[2]  # + np.random.random()
    signature = 0
    return [distance, bearing, signature, feature_coord[0], feature_coord[1]]


def estimate(real_pose, f_list):
    """
    :param real_pose: non estimated pose = [x,y,theta] of the robot (tricky sensor distance to feature calculation)
    :param f_list: features list (up to 3), where feature = [x, y]
    :return: estimated pose of the robot
    """
    landmarks = []
    for f in f_list:
        landmarks.append(feature(real_pose, f))

    # ToDo: add two landmark case (bilateration?)

    x, y = 0, 0
    if len(landmarks) == 3:
        x1 = landmarks[0][3]
        y1 = landmarks[0][4]
        r1 = landmarks[0][0]

        x2 = landmarks[1][3]
        y2 = landmarks[1][4]
        r2 = landmarks[1][0]

        x3 = landmarks[2][3]
        y3 = landmarks[2][4]
        r3 = landmarks[2][0]

        x, y = trilateration(x1, y1, r1, x2, y2, r2, x3, y3, r3)

    # ToDo: orientation estimation

    return [x, y]


def trilateration(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    a = 2 * x2 - 2 * x1
    b = 2 * y2 - 2 * y1
    c = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    d = 2 * x3 - 2 * x2
    e = 2 * y3 - 2 * y2
    f = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
    x = (c * e - f * b) / (e * a - b * d)
    y = (c * d - a * f) / (b * d - a * e)
    return x, y


# print(estimate([1, 1, np.deg2rad(30)], [[-1, 1], [3, 0], [1, 2]]))
