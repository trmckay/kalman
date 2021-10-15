from numpy.random import randn

_theta_r = 0
_theta_l = 0


async def read_encoder_l() -> float:
    return _theta_l + 3.1415 * randn()


async def read_encoder_r() -> float:
    return _theta_r + 3.1415 * randn()
