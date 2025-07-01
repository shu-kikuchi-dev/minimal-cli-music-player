import time
import vlc
from data_classes import Home, Artist, Album, Track

def play_album(album: Album):
    print(f"\nplaying album: {album.name}\n")
    for track in album.tracks:
        print(f"    now playing: {track.title}")
        player = vlc.MediaPlayer(str(track.path))
        player.play()
        time.sleep(2)
        while player.is_playing():
            time.sleep(1)