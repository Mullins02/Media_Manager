from constants import MEDIA_KEYWORDS 

class MediaDetector:
    @staticmethod
    def detect_type(directory: str, filename: str) -> str:
        directory = directory.lower()
        for media_type, keywords in MEDIA_KEYWORDS.items():
            for keyword in keywords:
                if keyword in directory:
                    return media_type 
        return "UNKNOWN"