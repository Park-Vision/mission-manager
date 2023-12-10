import asyncio
import pytest

from manager.decision.camera.mock_camera import MockCamera
from manager.decision.detector_decision import DetectorDecision
from manager.mission.waypoint import Waypoint

photo_paths = [
    {'path': 'drone_photos/example_photos/example1.jpg', 'expected_occupied': True},
    {'path': 'drone_photos/example_photos/example2.png', 'expected_occupied': True},
    {'path': 'drone_photos/example_photos/example3.png', 'expected_occupied': False}
]

@pytest.mark.asyncio
@pytest.mark.parametrize("photo_path", photo_paths)
async def test_detection(photo_path):
    decision = DetectorDecision(MockCamera(photo_path['path']))
    is_spot_occupied = await decision.decide(Waypoint(1, 51.118661117080116, 16.99027379987549))
    assert is_spot_occupied == photo_path['expected_occupied']
