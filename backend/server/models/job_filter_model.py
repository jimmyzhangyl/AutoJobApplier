from dataclasses import dataclass, field
from typing import List


@dataclass
class JobFilter:
    daysListed: int = 1  # default to 1 day if not specified by user
    titleIncludes: List[str] = field(default_factory=list)
    titleExcludes: List[str] = field(default_factory=list)
    locationIncludes: List[str] = field(default_factory=list)
    locationExcludes: List[str] = field(default_factory=list)
    typeExcludes: List[str] = field(default_factory=list)
    descriptionIncludes: List[str] = field(default_factory=list)
    descriptionExcludes: List[str] = field(default_factory=list)
    jobSource: List[str] = field(default_factory=list)
