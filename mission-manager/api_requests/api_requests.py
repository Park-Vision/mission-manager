import requests


def get_parking_spots(parking_id: int) -> list[dict]:
    """Make a request to API to get center points of all parking spots, to compose path"""
    r = requests.get(f"http://localhost:8080/api/parkingspots/drone/{parking_id}")

    if r.status_code == 200:
        return r.json()
