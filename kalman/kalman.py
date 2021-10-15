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
        """
        Create a Kalman filter.

        :param sensors: A map of string keys to asynchronous functions that return sensor data.

        :param sensor_cov: The sensor covariance matrix.

        :param kinematics: A dictionary that maps each state variable to it's calcution.

        :param state: List of state variables given as their name and initial value.

        :param state_cov: The state covariance matrix.

        Example::

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

            kf = KalmanFilter(sensors, sensor_cov, kinematics, state, state_cov)
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
        return str(self.dump_state())

    def state(self, k) -> float:
        return self._state[self._state_map[k]]

    def dump_state(self) -> list[tuple[str, float]]:
        state_vars = self._state_map.keys()
        return list(map(lambda k: (k, self.state(k)), state_vars))

    async def sensor(self, k) -> float:
        return await self._sensors_map[k]()

    async def predict(self):
        pass

    async def update(self):
        pass
