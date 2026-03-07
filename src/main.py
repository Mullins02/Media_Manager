import os, re
from pprint import pprint
import logging
import tkinter as tk

from constants import MEDIA_FOLDERS, VIDEO_EXTENSIONS

from utils.media_detector import MediaDetector
from utils.tmdb_helper import TMDB_Utils
from constants import FILE_EXTENSIONS_TO_SKIP, VIDEO_EXTENSIONS
from utils.lib_scanner import LibraryScanner
from ui import UIBackend, MediaManagerUI

from utils.logger import setup_logger

setup_logger(debug=False)

logger = logging.getLogger(__name__)

logger.info("Starting Media Manager")

def main():
    # test_files = [
    #     ("Media/Shows/The Office/Season 2", "The.Office.S02E03.WEBRip.mkv"),
    #     ("Media/Shows/Mr Inbetween", "Mr Inbetween - S01E01 - The Pee Pee Guy.mkv"),
    #     ("Media/Movies", "The.Dark.Knight.2008.1080p.mkv"),
    #     ("Media/Downloads", "random_file.mkv"),
    # ]W

    # for directory, filename in test_files:
    #     cleaner = MediaDetector.get_cleaner(directory, filename)

    #     print(f"Original: {filename}")

    #     if cleaner is None:
    #         print("Type: UNKNOWN")
    #         continue

    #     cleaned = cleaner.clean_filename()

    #     # TODO - compare the cleaned filname to tmdb
    #     print(f"Cleaned: {cleaned}\n")

    root = tk.Tk()
    app = MediaManagerUI(root)
    app.run()


def test():
    directory_paths = ["Z:\\Movies", "Z:\\Shows"]
    for directory_path in directory_paths:
        for root, dirs, files in os.walk(directory_path):
            base = next((b for b in MEDIA_FOLDERS if root.startswith(b)), None)

            if not base:
                continue

            relative = os.path.relpath(root, base)
            parts = relative.split(os.sep)

            if parts[0] == ".":
                continue
            show_name = parts[0]

            for file in files:
                print(file)
                cleaner = MediaDetector.get_cleaner(root, file)
                if cleaner is None:
                    continue
                cleaned = cleaner.clean_filename()
    print("end of test")


def test2():
    show_cache = {}
    tmdb = TMDB_Utils()
    directory_paths = ["Z:\\Shows"]
    for directory_path in directory_paths:
        for root, dirs, files in os.walk(directory_path):
            base = next((b for b in MEDIA_FOLDERS if root.startswith(b)), None)

            if not base:
                continue

            relative = os.path.relpath(root, base)
            parts = relative.split(os.sep)

            if parts[0] == ".":
                continue
            show_name = parts[0]

            if show_name not in show_cache:
                print(show_name)
                episodes = tmdb.get_episode_list(show_name=show_name)

                lookup = {}
                if episodes:
                    for ep in episodes:
                        key = f"S{ep['season_number']:02}E{ep['episode_number']:02}"
                        lookup[key] = ep

                show_cache[show_name] = lookup

            lookup = show_cache[show_name]

            for file in files:

                cleaner = MediaDetector.get_cleaner(root, file)

                if cleaner is None:
                    continue

                cleaned = cleaner.clean_filename()

                filename = cleaned["filename"]

                match = re.search(r"S\d{2}E\d{2}", filename)

                if match:
                    code = match.group(0).upper()

                    if code in lookup:
                        tmdb_ep = lookup[code]

                        print("Matched:")
                        print(f'\t{tmdb_ep["formatted_title"]}')
                        print("\tto")
                        print(f"\t{file}")

                    name_only, ext = os.path.splitext(file)
                    print(name_only)
                    print(tmdb_ep["formatted_title"])
                    if name_only == tmdb_ep["formatted_title"]:
                        print("\t\tfile can stay")
                    expected_filename = tmdb_ep["formatted_title"] + ext
                    if file != expected_filename:
                        print(
                            f"\t\tFile renamed {tmdb_ep["formatted_title"]+(file[-4:])}"
                        )
    print("end of test")
    
    
def test3():
    tmdb = TMDB_Utils()
    movie_cache = {}
    directory_paths = [r"Z:\Movies"]

    for directory_path in directory_paths:
        for root, dirs, files in os.walk(directory_path):
            base = next((b for b in MEDIA_FOLDERS if root.startswith(b)), None)

            if not base:
                continue

            for file in files:
                
                original_name_only, original_ext = os.path.splitext(file)
                
                if not original_ext in FILE_EXTENSIONS_TO_SKIP and original_ext in VIDEO_EXTENSIONS:
                    cleaner = MediaDetector.get_cleaner(root, file)

                    if cleaner is None:
                        continue

                    cleaned = cleaner.clean_filename()
                    cleaned_name = cleaned["filename"]

                    name_only, ext = os.path.splitext(cleaned_name)
                    name, year = name_only.split(" (")
                    year = year.split(")")[0]
                    
                    print(name, "------", year)

                    if name_only not in movie_cache:
                        movie_cache[name_only] = tmdb.get_movie_details(movie_name=name, year=year)

                    tmdb_movie = movie_cache[name_only]

                    if not tmdb_movie:
                        print(f"Could not find movie for: {file}")
                        continue

                    print("Matched:")
                    print(f'\t{tmdb_movie["formatted_title"]}')
                    print("\tto")
                    print(f"\t{file}")

                    original_name_only, original_ext = os.path.splitext(file)
                    expected_filename = tmdb_movie["formatted_title"] + original_ext

                    print(original_name_only)
                    print(tmdb_movie["formatted_title"])

                    if file == expected_filename:
                        print("\t\tfile can stay")
                    else:
                        print(f"\t\tFile renamed {expected_filename}")
                else:
                    print("file skipped")

    print("end of test")


if __name__ == "__main__":
    main()
    # test()
    # test2()
    # test3()
