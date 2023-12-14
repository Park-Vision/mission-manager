import os

from manager.decision.camera.camera import Camera


def check_if_path_is_dir(path: str) -> bool:
    if os.path.isfile(path):
        return False
    elif os.path.isdir(path):
        return True
    else:
        print(f"{path} does not exist.")
        return False


class MockCamera(Camera):
    """Mocks real camera"""

    def __init__(self, mock_photo_path: str = "unspecified") -> None:
        super().__init__()
        self.mock_photo_path = mock_photo_path
        # in directory mode, camera will cycle through all photos in directory
        # otherwise it will return same photo every time
        self.directory_mode = check_if_path_is_dir(self.mock_photo_path)
        if self.directory_mode:
            self.file_counter = 0

    def get_next_file_path(self):
        files = [file for file in os.listdir(self.mock_photo_path) if os.path.isfile(os.path.join(self.mock_photo_path, file))]

        # Get the next file path
        path = os.path.join(self.mock_photo_path, files[self.file_counter % len(files)])
        self.file_counter += 1

        return path

    async def take_photo(self) -> str:
        if self.mock_photo_path == "unspecified":
            return "drone_photos/example_photos/example1.jpg"
        elif self.directory_mode:
            # directory mode
            photo_path = self.get_next_file_path()
            print(f"Mock camera taking photo {photo_path}")
            return photo_path
        else:
            # one file mode
            return self.mock_photo_path
