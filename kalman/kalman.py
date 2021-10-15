from typing import Callable
from logging import info

import numpy as np

from .sensors import Sensor

class KalmanFilter:
    def __init__(
        self,
        sensors: dict[str, Sensor],
        sensor_cov: np.ndarray,
        kinematics: dict[str, Callable],
        state: list[tuple[str, float]],
        state_cov: np.ndarray,
    ):
        """Create a Kalman filter.

        Arguments:
            sensors {list[tuple[str, Sensor]]} -- A map of string keys to Sensors.

            sensor_cov {np.matrix} -- The sensor covariance matrix.

            kinematics {dict[str, Callable[[list], float]]}} -- A dictionary that maps
            state variables to a function that can be used to calculate them. The function
            will take the list of sensors and the state, and return a float.

            state {list[tuple[str, float]]} -- List of state variables given as their name
            and initial value.

            state_cov {np.matrix} -- The state covariance matrix.
        """

        # Covariance is NxN and there are N sensors.
        assert len(sensor_cov) == len(sensors)
        assert len(state_cov) == len(state)

        self._sensors = sensors
        self._sensor_map = {}
        for s in sensors:
            self._sensor_map[s[0]] =  s[1]

        self.sensor_cov = sensor_cov
        self.state_cov = state_cov

        self.kinematics = kinematics

        self._state = np.array([v[1] for v in state])
        self._state_map = {}
        for i, (v, _) in enumerate(state):
            self._state_map[v[0]] = i

    def state(self, k) -> float:
        return self._state[self._state_map[k]]

    def sensor(self, k) -> Sensor:
        return self._sensor_map[k].read()

    def predict(self):
        pass

    def update(self):
        pass
