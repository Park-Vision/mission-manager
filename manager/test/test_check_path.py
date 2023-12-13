import pytest

from manager.decision.camera.mock_camera import check_if_path_is_dir

paths = [
    {"path": "drone_photos/example_photos", "expected_is_dir": True},
    {"path": "manager/telemetry", "expected_is_dir": True},
    {"path": "drone_photos/example_photos/example3.png", "expected_is_dir": False},
    {"path": "manager/telemetry/encryption.py", "expected_is_dir": False},
]

@pytest.mark.parametrize("path", paths)
def test_detection(path):
    is_dir = check_if_path_is_dir(path['path'])
    assert is_dir == path["expected_is_dir"]
