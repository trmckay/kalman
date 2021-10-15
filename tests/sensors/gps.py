from numpy.random import randn

_position = (0, 0, 0)


async def read_gps_x() -> float:
    return _position[0] + 10 * randn()


async def read_gps_y() -> float:
    return _position[1] + 10 * randn()
