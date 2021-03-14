import numpy as np

def estimate(prev_mean, prev_covariance, action, sensor, orientation):
    """
    :param prev_mean: column np.array([[x], [y], [theta]]) from previous step
    :param prev_covariance: covariance matrix np.array([[a,0,0], [0,b,0], [0,0,c]]) from previous step
    :param action: u_t = np.array([[v], [w]])
    :param sensor: sensor estimation z_t = np.array([[x], [y], [theta]])
    :param orientation: current orientation of the robot in rad
    :return: estimated mean and covariance
    """
    R = np.array([[np.random.random(), 0, 0], [0, np.random.random(), 0], [0, 0, np.random.random()]])
    Q = np.array([[np.random.random(), 0, 0], [0, np.random.random(), 0], [0, 0, np.random.random()]])

    # prediction
    mean_pred = motion_prediction(prev_mean[0][0], prev_mean[1][0], prev_mean[2][0], orientation, action[0][0], action[1][0])
    covariance_pred = np.add(prev_covariance, R)

    # correction
    K = kalman_gain(covariance_pred, Q)
    mean = mean_estimation(mean_pred, K, sensor)
    covariance = covariance_estimation(K, covariance_pred)

    return mean, covariance

def motion_prediction(x_prev, y_prev, theta_prev, orientation, v, w):
    x = x_prev + v*np.cos(orientation)
    y = y_prev + v*np.sin(orientation)
    theta = theta_prev + w
    return np.array([[x], [y], [theta]])

def kalman_gain(covariance_pred, noise):
    inverse = np.linalg.inv(np.add(covariance_pred, noise))
    return np.dot(covariance_pred, inverse)

def mean_estimation(mean_pred, K, sensor):
    a = np.subtract(sensor, mean_pred)
    b = np.dot(K, a)
    return np.add(mean_pred, b)

def covariance_estimation(K, covariance_pred):
    return np.dot(np.subtract(np.identity(3), K), covariance_pred)


"""prev_mean = np.array([[300], [56], [np.deg2rad(50)]])
prev_covariance = np.array([[3,0,0], [0,2,0], [0,0,9]])
action = np.array([[10], [np.deg2rad(70)]])
sensor = np.array([[390], [50], [np.deg2rad(55)]])
orientation = np.deg2rad(74)
estimate(prev_mean, prev_covariance, action, sensor, orientation)"""
