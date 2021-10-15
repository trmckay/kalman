from typing import Callable, Any, Coroutine

import numpy as np


class KalmanFilter:
    def __init__(
        self,
        sensors: dict[str, Callable[[], Coroutine[Any, Any, float]]],
        sensor_cov: np.ndarray,
        kinematics: dict[
            str,
            Callable[["KalmanFilter"], float],
        ],
        state: list[tuple[str, float]],
        state_cov: np.ndarray,
    ):
        """Create a Kalman filter.

        Arguments:
            * `sensors`: A map of string keys to asynchronous functions that return sensor data.
            * `sensor_cov`: The sensor covariance matrix.
            * `kinematics`: A dictionary that maps state variables to a function that can be used
               to calculate them. The function will take the list of sensors and the state,
               and return a float.
            * `state`: List of state variables given as their name and initial value.
            * `state_cov`: The state covariance matrix.
        """

        # Covariance is NxN and there are N sensors.

        self._sensors_map = sensors

        self.sensor_cov = sensor_cov
        self.state_cov = state_cov

        self.kinematics = kinematics

        self._state = np.array([v[1] for v in state])
        self._state_map = {}
        for i, (v, _) in enumerate(state):
            self._state_map[v] = i

    def __repr__(self) -> str:
        state_vars = self._state_map.keys()
        state_vars = list(map(lambda k: (k, self.state(k)), state_vars))
        return str(state_vars)

    def state(self, k) -> float:
        return self._state[self._state_map[k]]

    def sensor(self, k) -> float:
        return self._sensor_map[k]()

    def predict(self):
        pass

    def update(self):
        pass
