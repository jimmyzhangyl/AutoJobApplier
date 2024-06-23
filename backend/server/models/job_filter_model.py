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

    # Check types of the fields, as field data as list in very important, passing as string will causing trouble but without any error
    def __post_init__(self):
        if not isinstance(self.titleIncludes, list) or not all(
            isinstance(item, str) for item in self.titleIncludes
        ):
            raise TypeError(
                f"titleIncludes must be a list of strings, got {self.titleIncludes}"
            )
        if not isinstance(self.titleExcludes, list) or not all(
            isinstance(item, str) for item in self.titleExcludes
        ):
            raise TypeError(
                f"titleExcludes must be a list of strings, got {self.titleExcludes}"
            )
        if not isinstance(self.locationIncludes, list) or not all(
            isinstance(item, str) for item in self.locationIncludes
        ):
            raise TypeError(
                f"locationIncludes must be a list of strings, got {self.locationIncludes}"
            )
        if not isinstance(self.locationExcludes, list) or not all(
            isinstance(item, str) for item in self.locationExcludes
        ):
            raise TypeError(
                f"locationExcludes must be a list of strings, got {self.locationExcludes}"
            )
        if not isinstance(self.typeExcludes, list) or not all(
            isinstance(item, str) for item in self.typeExcludes
        ):
            raise TypeError(
                f"typeExcludes must be a list of strings, got {self.typeExcludes}"
            )
        if not isinstance(self.descriptionIncludes, list) or not all(
            isinstance(item, str) for item in self.descriptionIncludes
        ):
            raise TypeError(
                f"descriptionIncludes must be a list of strings, got {self.descriptionIncludes}"
            )
        if not isinstance(self.descriptionExcludes, list) or not all(
            isinstance(item, str) for item in self.descriptionExcludes
        ):
            raise TypeError(
                f"descriptionExcludes must be a list of strings, got {self.descriptionExcludes}"
            )
        if not isinstance(self.jobSource, list) or not all(
            isinstance(item, str) for item in self.jobSource
        ):
            raise TypeError(
                f"jobSource must be a list of strings, got {self.jobSource}"
            )
        if not isinstance(self.daysListed, int):
            raise TypeError(f"daysListed must be an integer, got {self.daysListed}")
