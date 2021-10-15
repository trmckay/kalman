import pytest
import matplotlib.pyplot as plt
from pytest_cases import parametrize_with_cases


@parametrize_with_cases("filter", prefix="filter_")
@pytest.mark.parametrize("rounds", [10, 100, 1000])
def test_kalman(filter, rounds):
    state_vs_time = {}
    for k in filter._state_map.keys():
        state_vs_time[k] = []

    for _ in range(rounds):

        for k in filter._state_map.keys():
            state_vs_time[k].append(filter.state(k))

        filter.predict()
        filter.update()

    t = range(rounds)
    for k in filter._state_map.keys():
        plt.plot(t, state_vs_time[k])
        plt.title(f"{k} vs. time ({rounds} time-steps)")
        plt.xlabel("time")
        plt.ylabel(k)
        plt.show()
