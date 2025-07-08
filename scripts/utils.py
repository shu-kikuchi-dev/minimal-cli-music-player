import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from data_classes import Home, Artist, Album, Track


def serialize_path(obj):
    if isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, list):
        return [serialize_path(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: serialize_path(v) for k, v in obj.items()}
    else:
        return obj


def dataclass_to_dir(obj):
    if is_dataclass(obj):
        raw_dict = asdict(obj)
        return serialize_path(raw_dict)
    raise TypeError("obj is not a dataclass instance")


def save_library_to_json(library: Home, filepath: Path):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dataclass_to_dir(library), f, ensure_ascii=False, indent=2)


def dict_to_home(data: dict) -> Home:
    artists = []
    for a in data.get('artists', []):
        albums = []
        for al in a.get('albums', []):
            tracks = [Track(Path(t['path']), t['title']) for t in al.get('tracks', [])]
            albums.append(Album(al['name'], Path(al['path']), tracks))
        artists.append(Artist(a['name'], Path(a['path']), albums))
    return Home(Path(data['home_dir']), artists)


def load_library_from_json(filepath: Path) -> Home:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return dict_to_home(data)