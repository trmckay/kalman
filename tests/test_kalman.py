import pytest
import numpy as np

from kalman.sensors import Gps, Encoder
from kalman import KalmanFilter


@pytest.fixture(scope="function")
def gps(gps_randomness):
    gps = [
        Gps("x", randomness=gps_randomness),
        Gps("y", randomness=gps_randomness),
        Gps("z", randomness=3 * gps_randomness),
    ]
    yield gps


@pytest.fixture(scope="function")
def encoders(encoder_randomness):
    encoders = [Encoder(randomness=encoder_randomness) for _ in range(2)]
    yield encoders


@pytest.fixture(scope="function")
def filter(encoders, gps):
    # Sensors contributing to the filter, each with a name.
    sensors = {
       "gps_x": gps[0],
       "gps_y": gps[1],
       "gps_z": gps[2],
       "enc_l": encoders[0],
       "enc_r": encoders[1],
    }

    # Covariance matrix for the sensor readings.
    sensor_cov = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ])

    # State variables and their initial values.
    state = [
        ("x", 0),
        ("y", 2),
        ("z", 5),
        ("theta", 0),
    ]

    # Covariance matrix for the state variables.
    state_cov = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    # Kinematics model for the system.
    kinematics = {
        "x": lambda f: f.sensor("gps_x"),
        "y": lambda f: f.sensor("gps_y"),
        "z": lambda f: f.sensor("gps_z"),
        "theta": lambda f: f.sensor("enc_r"),
    }

    yield KalmanFilter(sensors, sensor_cov, kinematics, state, state_cov)

@pytest.mark.parametrize("gps_randomness", [1, 5, 10])
@pytest.mark.parametrize("encoder_randomness", [0.1, 0.5, 1])
class TestKalman:
    def test_kalman(self, filter, gps_randomness, encoder_randomness):
        assert filter.state("x") == 0
        assert filter.state("y") == 2
        assert filter.state("z") == 5
