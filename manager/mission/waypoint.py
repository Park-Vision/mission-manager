import logging


class Waypoint:
    def __init__(self, spot_id: int = -1, lat: float = 0.0, lon: float = 0.0) -> None:
        self.spot_id = spot_id
        self.position = (lat, lon)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Waypoint):
            return NotImplemented
        return self.position == other.position


def process_parking_message(msg: dict) -> list[Waypoint]:
    """Convert parking spots from kafka message to objects"""
    try:
        return [
            Waypoint(
                spot["parkingSpotId"], spot["centerLatitude"], spot["centerLongitude"]
            )
            for spot in msg["cords"]
        ]
    except TypeError:
        logging.error("No valid waypoints to visit")
        return []
