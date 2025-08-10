from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp4 import MP4
from pathlib import Path
import re
import os


# check path existence and validity
def prompt_directory(message: str) -> Path:
    path = Path(input(message).strip()).resolve()
    if not path.exists() or not path.is_dir():
        print(f"\ninvalid directory: {path}\n")
        exit(1)
    return path


# select whether to run in bulk album mode or indivisual mode
def ask_all_or_not():
    while True:
        print("\nwhich mode would you want to execute?:")
        print("\n   1.remove all album's tags from home dir(type 'all')")
        print("\n   2.remove one album's tags from specific dir(type 'spe')")
        user_input = input("\n>>").strip()

        if user_input == "all":
            return True
        elif user_input == "spe":
            return False
        else:
            print("\ninvalid input. please enter again.\n")


# bulk album mode
def remove_all_albums(root_dir: Path):
    for album_dir in root_dir.iterdir():
        if album_dir.is_dir():
            print(f"\n=== Processing album: {album_dir.name} ===")
            remove_tags_in_directory(album_dir)
            rename_files_in_directory(album_dir)
        else:
            print(f"\nskipped (not a directory): {album_dir.name}\n")


# remove ID3 tags
def remove_id3_tags(mp3_path: Path):
    try:
        audio = MP3(mp3_path, ID3=ID3)
        audio.delete()
        audio.save()
        print(f"removed tags: {mp3_path}")
    except ID3NoHeaderError:
        print(f"no tags found: {mp3_path}")
    except Exception as e:
        print(f"failed to process {mp3_path}: {e}")


# remove M4A tags
def remove_m4a_tags(m4a_path: Path):
    try:
        audio = MP4(m4a_path)
        audio.clear()
        audio.save()
        print(f"removed tags: {m4a_path}")
    except Exception as e:
        print(f"failed to process {m4a_path}: {e}")


# search for supported files in the directory
def remove_tags_in_directory(root_dir: Path):
    try:
        for mp3_file in root_dir.rglob("*.mp3"):
            remove_id3_tags(mp3_file)
        for m4a_files in root_dir.rglob("*.m4a"):
            remove_m4a_tags(m4a_files)
    except Exception as e:
        print(f"error processing {root_dir}: {e}")


# some music apps prepend the disc num to the music file, but this 
# goes against the philosphy of simple music player.
def rename_files_in_directory(root_dir: Path):
    for ext in ("*.mp3", "*.m4a"):
        for file_path in root_dir.rglob(ext):
            original_name = file_path.name
            # check if the file name starts with a digit followed by a hyphen
            if re.match(r"^\d+-", original_name):
                new_name = re.sub(r"^\d+-", "", original_name)
                new_path = file_path.with_name(new_name)
                try:
                    file_path.rename(new_path)
                    print(f"renamed {original_name} -> {new_name}")
                except Exception as e:
                    print(f"failed to rename {original_name}: {e}")
            else:
                print(f"skipped (no  match): {original_name}")


# main function
def main():
    all_mode = ask_all_or_not()
    if all_mode:
        target_dir = prompt_directory("\nspecify home directory containing several albums.\n")
        remove_all_albums(target_dir)
    else:
        target_dir = prompt_directory("\nspecify the root dir for each albums.\n")
        remove_tags_in_directory(target_dir)
        rename_files_in_directory(target_dir)


if __name__ == "__main__":
    main()