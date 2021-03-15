"""Robotic Simulation Software Kalman Filter
Authors:
Sergi Nogues Farres
"""
import numpy as np


def estimate(prev_mean, prev_covariance, action, sensor):
    """
    :param prev_mean: column np.array([[x], [y], [theta]]) from previous step
    :param prev_covariance: covariance matrix np.array([[a,0,0], [0,b,0], [0,0,c]]) from previous step
    :param action: u_t = np.array([[v], [w]])
    :param sensor: sensor estimation z_t = np.array([[x], [y], [theta]])
    :return: estimated mean and covariance
    """
    # noise
    R = np.array([[np.random.normal(prev_mean[0][0]), 0, 0],
                  [0, np.random.normal(prev_mean[1][0]), 0],
                  [0, 0, np.random.normal(prev_mean[2][0])]])
    Q = np.array([[np.random.normal(sensor[0][0]), 0, 0],
                  [0, np.random.normal(sensor[1][0]), 0],
                  [0, 0, np.random.normal(sensor[2][0])]])

    pose_noise = np.random.multivariate_normal(prev_mean.T[0], R)
    sensor_noise = np.random.multivariate_normal(sensor.T[0], Q)

    B = np.array([[sensor_noise[0]*np.cos(prev_mean[2][0]), 0],
                  [sensor_noise[1]*np.sin(prev_mean[2][0]), 0],
                  [0, sensor_noise[2]]])

    # prediction
    mean_pred = motion_prediction(np.identity(3), prev_mean, B, action)
    covariance_pred = np.add(prev_covariance, R)

    # correction
    K = kalman_gain(covariance_pred, Q)
    mean = mean_estimation(mean_pred, K, sensor)
    covariance = covariance_estimation(K, covariance_pred)

    return mean, covariance


def motion_prediction(A, prev_mean, B, action):
    a = np.dot(A, prev_mean)
    b = np.dot(B, action)
    return np.add(a, b)


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
estimate(prev_mean, prev_covariance, action, sensor)"""
