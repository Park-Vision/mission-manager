class Waypoint:
    def __init__(self, spot_id: int, lat: float, lon: float) -> None:
        self.spot_id = spot_id
        self.position = (lat, lon)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Waypoint):
            return NotImplemented
        return self.position == other.position


def process_parking_json(json: list) -> list[Waypoint]:
    """Convert parking spots from database to objects"""
    waypoints = [
        Waypoint(spot["parkingSpotId"], spot["centerLatitude"], spot["centerLongitude"])
        for spot in json
    ]

    return waypoints
