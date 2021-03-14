import numpy as np

def feature(pose, feature_coord ):
    """
    :param feature_coord: feature [x, y]
    :param pose: robot pose [x y, theta]
    :return: [distance, bearing, signature]
    """
    # ToDo: properly calculate noise and define signature
    distance = np.sqrt((feature_coord[0] - pose[0])**2 + (feature_coord[1] - pose[1])**2) + np.random.random()
    bearing = np.arctan2(feature_coord[1] - pose[1], feature_coord[0] - pose[0]) - pose[2] + np.random.random()
    signature = np.random.random() + np.random.random()
    return distance, bearing, signature

def estimate():
    """
    Estimate pose of the robot by triangulation of feature list (up to 3)
    :return:
    """
    return None
