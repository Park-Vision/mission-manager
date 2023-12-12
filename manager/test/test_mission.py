import json
import time
from dataclasses import asdict

from manager.mission.mission import Mission, MissionStatus


def test_json_creation():
    spots = [
        {"parking_spot_id": 1, "occupied": True},
        {"parking_spot_id": 2, "occupied": True},
        {"parking_spot_id": 3, "occupied": True},
        {"parking_spot_id": 4, "occupied": False},
    ]
    test_mission = Mission(
        int(time.time()) - 1000, int(time.time()), MissionStatus.FINISHED, spots
    )

    mission_message = asdict(test_mission)
    mission_message["type"] = "missionResult"

    assert mission_message["status"] == "FINISHED"
