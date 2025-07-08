from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
from pathlib import Path
import re


def remove_id3_tags(mp3_path: Path):
    try:
        audio = MP3(mp3_path, ID3=ID3)
        audio.delete()
        audio.save()
        print(f"removed tags: {mp3_path}")
    except ID3NoHeaderError:
        print(f"\nno tags found: {mp3_path}\n")
    except Exception as e:
        print(f"\nfailed to process {mp3_path}: {e}\n")


def remove_tags_in_directory(root_dir: Path):
    if not root_dir.exists() or not root_dir.is_dir():
        print(f"\ninvalid directory: {root_dir}\n")
        return 
    for mp3_file in root_dir.rglob("*.mp3"):
        remove_id3_tags(mp3_file)


# some music apps prepend the disc num to the music file, but this 
# goes against the philosphy of simple music player.
def rename_files_in_directory(root_dir: Path):
    for mp3_file in root_dir.rglob("*.mp3"):
        original_name = mp3_file.name
        # check if the file name starts with a digit followed by a hyphen
        if re.match(r"^\d+-", original_name):
            new_name = re.sub(r"^\d+-", "", original_name)
            new_path = mp3_file.with_name(new_name)
            try:
                mp3_file.rename(new_path)
                print(f"renamed {original_name} -> {new_name}")
            except Exception as e:
                print(f"failed to rename {original_name}: {e}")
        else:
            print(f"skipped (no match): {original_name}")


def main():
    target_dir = input("\nspecify the root directory containing MP3 files to remove ID3 tags.\n>>").strip()
    target_dir = Path(target_dir).resolve()
    remove_tags_in_directory(target_dir)
    rename_files_in_directory(target_dir)


if __name__ == "__main__":
    main()