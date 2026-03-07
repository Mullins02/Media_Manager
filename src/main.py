import os

from constants import MEDIA_FOLDERS, VIDEO_EXTENSIONS

from media_detector import MediaDetector


def main():
    test_files = [
        ("Media/Shows/The Office/Season 2", "The.Office.S02E03.WEBRip.mkv"),
        ("Media/Shows/The Office", "The Office - S02E03 - bubble.mkv"),
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
        print(f"Cleaned: {cleaned}\n")
    
        
def test():
    directory_paths = ['Z:\\Movies', 'Z:\\Shows']
    for directory_path in directory_paths:
        for root, dirs, files in os.walk(directory_path):
            if root.startswith(tuple(MEDIA_FOLDERS)):
                for file in files:                    
                    cleaner = MediaDetector.get_cleaner(root, file)
                    print(f"Original: {file}")
                    if cleaner is None:
                        print("Type: UNKNOWN")
                        continue
                    cleaned = cleaner.clean_filename()
                    print(f'Cleaned: {cleaned}\n')
    print('end of test')


if __name__ == "__main__":
    main()
    # test()