from manager.decision.camera.camera import Camera


class MockCamera(Camera):
    """Mocks real camera"""

    def __init__(self, mock_photo_path: str = "unspecified") -> None:
        super().__init__()
        self.mock_photo_path = mock_photo_path

    async def take_photo(self) -> str:
        if self.mock_photo_path == "unspecified":
            return "drone_photos/example_photos/example1.jpg"
        else:
            return self.mock_photo_path
