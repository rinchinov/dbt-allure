from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Link:
    type: str
    name: str
    url: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Label:
    name: str
    value: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Step:
    name: str
    status: str
    start: int
    stop: int

    def to_dict(self):
        return asdict(self)


@dataclass
class TestCase:
    uuid: str
    historyId: str
    testCaseId: str
    fullName: str
    name: str
    status: str
    start: int
    stop: int
    links: List[Link] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)
    steps: List[Step] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
