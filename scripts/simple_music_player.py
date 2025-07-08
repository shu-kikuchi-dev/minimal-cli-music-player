import os
from pathlib import Path
from music_library import load_music_library
from utils import save_library_to_json, load_library_from_json
from data_classes import Home, Artist, Album, Track
from play_music import play_album


# ask for home dir
def ask_for_home_dir() -> str:
    default_home_dir = Path(r"C:\Users\shuki\Music\simple_music_player")
    home_dir_input = ""

    while True:
        user_input = input(
            f"\nspecify arbitrary home dir, or you can choose default dir({default_home_dir}) by entering 'd'.\n>>"
            ).strip()

        if user_input == 'd':
            home_dir_input = default_home_dir
        else:
            home_dir_input = Path(user_input)
            if not home_dir_input.is_dir():
                print("\ninvalib dir. please enter again.\n")
                continue

        while True:
            yn_input = input(
                f"\nyour home dir is '{home_dir_input}', are you sure? (y/n)\n>>"
                ).strip().lower()

            if yn_input == 'y':
                return home_dir_input
                break
            elif yn_input == 'n':
                print("\nOK. you can enter again.\n")
                break
            else:
                print("\ninvalib input. please enter again.\n")
                continue


# ask for load home dir or not
def ask_for_load_home(json_path: Path):
    while True:
        user_input = input(
            f"\ndo you want to reload your home dir and make json file?(y/n)\n>>"
            ).strip().lower()

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("\ninvalid input. please enter again.\n")


# choose artist
def choose_artist(home: Home) -> Artist:
    print("\nselect artist:\n")
    for i, artist in enumerate(home.artists):
        print(f"[{i}] {artist.name}")
    idx = int(input(">>"))
    return home.artists[idx]


# choose album from artist
def choose_album(artist: Artist) -> Album:
    print("\nselect album from artist: {artist.name}\n")
    for i, album in enumerate(artist.albums):
        print(f"[{i}] {album.name}")
    idx = int(input(">>"))
    return artist.albums[idx]


# main cli flow
def main():
    json_path = Path(__file__).parent.parent / "json" / "music_library.json"

    home_dir = ask_for_home_dir()
    print(f"\nyour home dir: {home_dir}\n")
    reload_flag = ask_for_load_home(json_path)

    if reload_flag:
        home = load_music_library(home_dir)
        save_library_to_json(home, json_path)
    else:
        if json_path.exists():
            home = load_library_from_json(json_path)
        else:
            print("\nno saved json found. loading from home dir...\n")
            home = load_music_library(home_dir)
            save_library_to_json(home, json_path)

    print(home)

    artist = choose_artist(home)
    album = choose_album(artist)
    play_album(album)


if __name__=="__main__":
    main()