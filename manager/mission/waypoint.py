class Waypoint:
    def __init__(self, spot_id: int = -1, lat: float = 0.0, lon: float = 0.0) -> None:
        self.spot_id = spot_id
        self.position = (lat, lon)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Waypoint):
            return NotImplemented
        return self.position == other.position


def process_parking_json(json: list) -> list[Waypoint]:
    """Convert parking spots from database to objects"""
    try:
        return [
            Waypoint(
                spot["parkingSpotId"], spot["centerLatitude"], spot["centerLongitude"]
            )
            for spot in json
        ]
    except TypeError:
        print("No valid waypoints to visit")
        return []
