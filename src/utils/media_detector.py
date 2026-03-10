from constants import MEDIA_KEYWORDS
from cleaners import CLEANERS


class MediaDetector:
    @staticmethod
    def detect_type(directory: str, filename: str) -> str:
        directory = directory.lower()
        for media_type, keywords in MEDIA_KEYWORDS.items():
            for keyword in keywords:
                if keyword in directory:
                    return media_type
        return "UNKNOWN"

    @staticmethod
    def get_media_type_and_file_utils(directory: str, filename: str) -> tuple:
        media_type = MediaDetector.detect_type(directory, filename)
        cleaner_class = CLEANERS[media_type]
        if cleaner_class is None:
            return None, None
        return media_type, cleaner_class(directory, filename)
