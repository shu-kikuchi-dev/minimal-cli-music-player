import os
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

### ask for home dir
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

## ask for load home dir or not
def ask_for_load_home():
    default_json_dir = Path(r"C:\Users\shuki\Projects\hobby\Scripts\Python\simple_music_player\json")
    
    while True:
        user_input = input(
            f"do you want to reload your home dir and make json file?(y/n)\n>>"
            ).strip().lower()

        if user_input == 'y':
            # call loading home dir function and make json
            pass
        elif user_input == 'n':
            break
        else:
            print("invalid input. please enter again.\n")
            continue


def main():
    home_dir = ask_for_home_dir()
    print(f"\nyour home dir: {home_dir}\n")
    ask_for_load_home()

if __name__=="__main__":
    main()