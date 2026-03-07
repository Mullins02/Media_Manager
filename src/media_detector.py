from constants import MEDIA_KEYWORDS
from cleaners import CLEANERS


class MediaDetector:
    @staticmethod
    def _detect_type(directory: str, filename: str) -> str:
        directory = directory.lower()
        for media_type, keywords in MEDIA_KEYWORDS.items():
            for keyword in keywords:
                if keyword in directory:
                    return media_type
        return "UNKNOWN"

    @staticmethod
    def get_cleaner(directory: str, filename: str):
        media_type = MediaDetector._detect_type(directory, filename)
        cleaner_class = CLEANERS[media_type]
        if cleaner_class is None:
            return None
        return cleaner_class(directory, filename)
