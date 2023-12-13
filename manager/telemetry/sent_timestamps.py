from dataclasses import dataclass


@dataclass
class SentTimestamps:
    """Keeps track of intervals between sending data to server"""

    stage: float = 1
    position: float = 1
    sys_status: float = 1
    gps_status: float = 1
