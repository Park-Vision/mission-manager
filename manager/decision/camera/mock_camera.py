from manager.decision.camera.camera import Camera


class MockCamera(Camera):
    """Mocks real camera"""
    def __init__(self) -> None:
        super().__init__()
    
    async def take_photo(self) -> str:
        return "drone_photos/example_photos/example1.jpg"
