from math import pi

from numpy.random import randn

from .sensor import Sensor


class Encoder(Sensor):
    def __init__(self, theta_i=0, randomness=10):
        self.theta = theta_i
        self.randomness = randomness

    def read(self) -> float:
        return (self.theta + (self.randomness * randn())) % (2 * pi)
