from typing import Callable

import numpy as np


class Sensor:
    def read(self) -> float:
        return 0.0

    def update(self, state: dict):
        """
        Save all state variables to the Sensor object.
        """

        for k, v in [(k, state[k]) for k in state.keys()]:
            setattr(self, k, v)
