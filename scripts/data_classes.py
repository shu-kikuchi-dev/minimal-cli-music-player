from dataclasses import dataclass, field
from pathlib import Path
from typing import List


### dedine data class
@dataclass
class Track:
    path: Path
    title: str

@dataclass
class Album:
    name: str
    path: Path
    tracks: List[Track] = field(default_factory=list)

@dataclass
class Artist:
    name: str
    path: Path
    albums: List[Album] = field(default_factory=list)

@dataclass
class Home:
    home_dir: Path
    artists: List[Artist] = field(default_factory=list)