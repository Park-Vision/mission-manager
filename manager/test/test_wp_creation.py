from manager.mission.waypoint import Waypoint, process_parking_message

input = {
    "cords": [
        {
            "parkingSpotId": 1,
            "centerLatitude": 51.118661117080116,
            "centerLongitude": 16.99027379987549,
        },
        {
            "parkingSpotId": 2,
            "centerLatitude": 51.11861444757546,
            "centerLongitude": 16.990350912447425,
        },
    ]
}

correct_output = [
    Waypoint(1, 51.118661117080116, 16.99027379987549),
    Waypoint(2, 51.11861444757546, 16.990350912447425),
]


def test_wp():
    # Test processing parking spot json message
    waypoints = process_parking_message(input)
    assert waypoints == correct_output
