import os

from constants import MEDIA_FOLDERS, VIDEO_EXTENSIONS

from media_detector import MediaDetector


def main():
    test_files = [
        ("Media/Shows/The Office/Season 2", "The.Office.S02E03.WEBRip.mkv"),
        ("Media/Shows/Mr Inbetween", "Mr Inbetween - S01E01 - The Pee Pee Guy.mkv"),
        ("Media/Movies", "The.Dark.Knight.2008.1080p.mkv"),
        ("Media/Downloads", "random_file.mkv"),
    ]

    for directory, filename in test_files:
        cleaner = MediaDetector.get_cleaner(directory, filename)
        

        print(f"Original: {filename}")

        if cleaner is None:
            print("Type: UNKNOWN")
            continue

        cleaned = cleaner.clean_filename()
        
        #TODO - compare the cleaned filname to tmdb 
        print(f"Cleaned: {cleaned}\n")


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

if __name__ == "__main__":
    main()
    # test()
