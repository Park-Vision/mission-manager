from manager.mission.path import create_path
from manager.mission.waypoint import Waypoint

LANDING_POINT = (51.11016, 17.05963)


correct_order = [
    LANDING_POINT,
    (51.11016, 17.05936),
    (51.11002, 17.0591),
    (51.10977, 17.05894),
    (51.10987, 17.05903),
    (51.10996, 17.05923),
    LANDING_POINT,
]

points = [
    LANDING_POINT,
    (51.11016, 17.05936),
    (51.10977, 17.05894),
    (51.10987, 17.05903),
    (51.10996, 17.05923),
    (51.11002, 17.0591),
]


def test_path():
    points_waypoints = [Waypoint(0, point[0], point[1]) for point in points]
    correct_order_waypoints = [
        Waypoint(0, point[0], point[1]) for point in correct_order
    ]

    path = create_path(points_waypoints)
    assert path == correct_order_waypoints


test_path()
