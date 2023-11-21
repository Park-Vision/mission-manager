from random import shuffle

import pytest

from manager.mission.path import create_path
from manager.mission.waypoint import Waypoint

LANDING_POINT = (51.11016, 17.05963)


correct_order_1 = [
    LANDING_POINT,
    (51.11016, 17.05936),
    (51.11002, 17.0591),
    (51.10977, 17.05894),
    (51.10987, 17.05903),
    (51.10996, 17.05923),
    LANDING_POINT,
]

correct_order_2 = [
    LANDING_POINT,
    (51.110965793535975, 16.87588381999903),
    (51.11194843653306, 16.87352422484061),
    (51.112464439189026, 16.871782057081067),
    (51.11273231388913, 16.870989626376424),
    LANDING_POINT,
]


@pytest.mark.parametrize("correct_order", [correct_order_1, correct_order_2])
def test_path(correct_order):
    correct_order_waypoints = [
        Waypoint(0, point[0], point[1]) for point in correct_order
    ]

    # Randomize order
    input_points = [p for p in correct_order if p != LANDING_POINT]
    shuffle(input_points)
    # Landing point needs to be first, otherwise
    # path could start from the opposite side
    input_points.insert(0, LANDING_POINT)

    path = create_path([Waypoint(0, point[0], point[1]) for point in input_points])
    assert path == correct_order_waypoints
