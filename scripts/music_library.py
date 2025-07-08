from pathlib import Path
from data_classes import Home, Artist, Album, Track


def load_music_library(home_dir: Path) -> Home:
    home = Home(home_dir=home_dir)
    artists_root = home_dir / "Artists"

    if not artists_root.exists():
        print(f"\nwarning: expected 'Artists' folder not found in {home_dir}\n")
        return home

    for artist_path in artists_root.iterdir():
        if artist_path.is_dir():
            artist = Artist(name=artist_path.name, path=artist_path)
            for album_path in artist_path.iterdir():
                if album_path.is_dir():
                    album = Album(name=album_path.name, path=album_path)
                    for track_path in album_path.iterdir():
                        if track_path.is_file() and track_path.suffix.lower() in ['.mp3', '.wav']:
                            track = Track(path=track_path, title=track_path.stem)
                            album.tracks.append(track)
                    artist.albums.append(album)
            home.artists.append(artist)
    return home