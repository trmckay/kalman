from numpy.random import randn

from .sensor import Sensor


class Gps(Sensor):
    def __init__(self, axis: str, initial: float = 0, randomness: int = 10):
        self.axis = axis
        self.randomness = randomness
        setattr(self, axis, initial)

    def read(self) -> float:
        return getattr(self, self.axis, self.randomness * randn())
