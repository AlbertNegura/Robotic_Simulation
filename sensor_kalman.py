"""Robotic Simulation Software Sensor model for Localization
Authors:
Sergi Nogues Farres
"""
import numpy as np
import utils


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

    position = []
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

        position = utils.trilateration(x1, y1, r1, x2, y2, r2, x3, y3, r3)

    elif len(landmarks) == 2:
        x1 = landmarks[0][3]
        y1 = landmarks[0][4]
        r1 = landmarks[0][0]

        x2 = landmarks[1][3]
        y2 = landmarks[1][4]
        r2 = landmarks[1][0]

        position = utils.bilateration(x1, y1, r1, x2, y2, r2)

    # ToDo: orientation estimation

    return position


"""pose = [1, 1, np.deg2rad(30)]
p1 = [-1, 1]
p2 = [3, 0]
p3 = [1, 2]
print(estimate(pose, [p1, p2, p3]))
print(estimate(pose, [p1, p2]))"""
