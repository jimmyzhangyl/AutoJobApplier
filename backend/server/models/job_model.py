from dataclasses import dataclass


@dataclass
class Job:
    id: int
    title: str
    location: str
    description: str
    listedDate: str
    type: str
    quickApplySupported: bool
    url: str
