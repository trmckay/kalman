import numpy as np

from tests.sensors import (
    read_gps_x,
    read_gps_y,
    read_encoder_l,
    read_encoder_r,
)
from kalman import KalmanFilter


def filter_case_1():
    # Sensors contributing to the filter, each with a name.
    sensors = {
        "gps_x": read_gps_x,
        "gps_y": read_gps_y,
        "enc_l": read_encoder_l,
        "enc_r": read_encoder_r,
    }

    # Covariance matrix for the sensor readings.
    sensor_cov = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # State variables and their initial values.
    state = [
        ("x", 0),
        ("y", 2),
        ("theta", 0),
    ]

    # Covariance matrix for the state variables.
    state_cov = np.array(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0],
        ]
    )

    # Kinematics model for the system.
    kinematics = {
        "x": lambda f: f.sensor("gps_x"),
        "y": lambda f: f.sensor("gps_y"),
        "theta": lambda f: f.sensor("enc_r"),
    }

    return KalmanFilter(sensors, sensor_cov, kinematics, state, state_cov)
