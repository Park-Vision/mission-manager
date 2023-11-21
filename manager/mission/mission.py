import enum
from dataclasses import dataclass, field


class MissionStatus(str, enum.Enum):
    CREATED = "CREATED"
    ONGOING = "ONGOING"
    FINISHED = "FINISHED"
    INTERRUPTED = "INTERRUPTED"


@dataclass
class Mission:
    """Keeps track of drone mission"""

    start_timestamp: int = 1
    end_timestamp: int = 2
    status: MissionStatus = MissionStatus.CREATED
    free_spots: list[dict] = field(default_factory=list)
